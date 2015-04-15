from copy import deepcopy
import datetime
from collections import namedtuple
from pupa.scrape import Scraper, Person, Organization, Event  

class MarylandContributionScraperException(Exception):
    pass

class MarylandContributionsScraper(Scraper):
    business_contribution_types = ['Ballot Issue Committee', 
                                   'Business/Group/Organization', 
                                   'Candidate Committee',
                                   'Federal Committee', 
                                   'Financial Institution',
                                   'Labor Union', 
                                   'Legislative Caucus Committee',
                                   'Lump Sum', 
                                   'Non-Profit Organization', 
                                   'PAC Committee', 
                                   'Party Central',
                                   'Political Club', 
                                   'Public Contribution', 
                                   'Registered Out-of-State Non-Federal Committee',
                                   'Reimburse', 
                                   'Slate Committee',
                                   'Unregistered Out-of-State Non-Federal Committee']
    individual_contribution_types = ['Individual', 
                                     'Individual - Matching fund request', 
                                     'Spouse (Candidate)', 
                                     'Self (Candidate)']
    search_url = 'https://campaignfinancemd.us/Public/ViewReceipts?theme=vista'
    csv_url = 'https://campaignfinancemd.us/Public/ExportCSVNew?page=1&orderBy=~&filter=~&Grid-size=15&theme=vista'
    csv_header_row = 'Contribution Date,Contributor Name,Contributor Address,Contributor Type,Employer Name,Employer Occupation,Contribution Type,Contribution Amount,Receiving Committee,Filing Period,Office,Fundtype,'
    days_between = 30
    def scrape(self):
        """
        Upon accessing the search page you're given a cookie that 
        maintains your state through the website. This allows
        the server to know what csv data to send when you request it
        """
        today = datetime.datetime.today()
        start_day = datetime.datetime(1994, 1, 1, 0, 0) 
        delta_days = datetime.timedelta(days=self.days_between)
        end_day = start_day + delta_days
        while end_day < today:
            csv_data = self.search_date_range_csv(start_day, end_day)
            if csv_data:
                for result_objects in self.categorize_data(csv_data):
                    yield from result_objects
            start_day = end_day
            end_day = end_day + delta_days

        #now handle last few days up to today
        csv_data = self.search_date_range_csv(start_day, today)
        #result_objects = self.categorize_data(csv_data)  
        for result_objects in self.categorize_data(csv_data):
            yield from result_objects      

    def categorize_data(self, csv_data):
        return_objs = []
        Contribution = namedtuple('Contribution', self.csv_header_row.replace(' ', '_'))
        for line in csv_data.split('\n'): # explicity defining delimiter because otherwise fails in case of single line
            if not line:
                continue

            # cur_obj will be the person or organization that made the contribution
            cur_obj = None
            contribution = Contribution(*line.split(','))
            
            if contribution.Contributor_Type in self.business_contribution_types:
                cur_obj = Organization(contribution.Contributor_Name)
            elif contribution.Contributor_Type in self.individual_contribution_types:
                cur_obj = Person(contribution.Contributor_Name)
            elif contribution.Contributor_Type == 'Unknown/Anonymous':
                if contribution.Contributor_Name: #ignoring un-named contributors
                    #these look like catch-all business contributions
                    cur_obj = Organization(contribution.Contributor_Name)
            if cur_obj: 
                #we don't set cur_obj in the event that there was an 
                #anonymous/unknown contribution without a Contribution_Name
                #so we need to check that it exists before adding to it
                cur_obj.add_source(url=self.search_url)
                cur_obj.source_identified = True
                if contribution.Contributor_Address:
                    cur_obj.add_contact_detail(type='address', value=contribution.Contributor_Address)
                if contribution.Employer_Name:
                    cur_obj.extras['Employer'] = contribution.Employer_Name
                if contribution.Employer_Occupation:
                    cur_obj.extras['Occupation'] = contribution.Employer_Occupation
                
                #recipiant_obj is the organization that received the contribution
                recipiant_obj = Organization(contribution.Receiving_Committee)  
                recipiant_obj.extras['Office'] = contribution.Office
                recipiant_obj.extras['Filing Period'] = contribution.Filing_Period
                recipiant_obj.extras['Fundtype'] = contribution.Fundtype

                #transaction is the event linking the donor and recipiant
                transaction = Event('Contribution', contribution.Contribution_Date, 'EST', 'Maryland') #EST and Maryland b/c MD
                transaction.extras['Contribution Amount'] = contribution.Contribution_Amount
                transaction.extras['Contribution Type'] = contribution.Contribution_Type
                transaction.add_source(url=self.search_url)
                #transaction.source_identified = True
                transaction.participants.append(cur_obj.as_dict())
                transaction.participants.append(recipiant_obj.as_dict())
                yield (cur_obj, recipiant_obj, transaction)        
            else:
                yield []
 
    def search_date_range_csv(self, start_day, end_day):
        # start_date and end_date are datetime objects
        date_range_params = {'dtStartDate': datetime.datetime.strftime(start_day, '%m/%d/%Y'),
                                 'dtEndDate':  datetime.datetime.strftime(end_day, '%m/%d/%Y')}
        post_data = self.generate_post_params(date_range_params)
        search_resp = self.post(self.search_url, data=post_data)
        if not (200 <= search_resp.status_code < 300):
            raise MarylandContributionScraperException('Unsuccessful response to search parameter posting')
        csv_resp = self.get(self.csv_url, stream=True)
        if not (200 <= csv_resp.status_code < 300):
            raise MarylandContributionScraperException('Unsuccessful attempt to get CSV file after successful search submission')
        if not csv_resp.text.startswith(self.csv_header_row):
            raise MarylandContributionScraperException('CSV file format does not have expected header')
        #strip out the header since we already know it's there and what's in it
        ind = csv_resp.text.find('\n')
        if (ind == len(csv_resp.text)-1) or (ind == -1):
            return None
        else:
            return csv_resp.text[ind+1:]        

    def generate_post_params (self, params):
        # params is a dict containing only the parameters to be set 
        # all others default to None, except btnSearch which must be set to 'Search'
        unset_params = {'txtContributorName': None,
                         'txtFirstName': None,
                         'txtStreet': None,
                         'txtTown': None,
                         'ddlState': None,
                         'txtZipCode': None,
                         'txtZipExt': None,
                         'ContributorType': None,
                         'ContributionType': None,
                         'MemberId': None,
                         'FilingYear=': None,
                         'FilingPeriodName': None,
                         'dtStartDate': None,
                         'dtEndDate': None,
                         'txtAmountRangeFrom': None,
                         'txtAmountRangeTo': None,
                         'txtReceivingRegistrant': None,
                         'ddlOfficeType': None,
                         'ddlOfficeSought': None,
                         'ddljurisdiction': None,
                         'ddlEmployerOccupation': None,
                         'ddlFundType': None,
                         'btnSearch': 'Search'}

        post_data = deepcopy(unset_params)
        post_data.update(params)
        return post_data

