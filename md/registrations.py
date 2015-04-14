import re

from pupa.scrape import Scraper, Person, Membership
from utils.lxmlize import LXMLMixin

class MarylandRegistrationScraper(Scraper, LXMLMixin):
    ''' https://campaignfinancemd.us/Public/ViewCommittees
    '''

    search_url = 'https://campaignfinancemd.us/Public/Search?theme=vista'
    committee_url = 'https://campaignfinancemd.us/Public/_ViewCommittees?theme=vista'
    member_url = 'https://campaignfinancemd.us/Public/ShowReview?memberID={MemberID}&memVersID={MemberVersID}&cTypeCode={CommitteeTypeCode}'
    results_rex = re.compile('Displaying items (?P<first>\d+) - (?P<last>\d+) of (?P<total>\d+)')

    def scrape(self):
        for reg in self.crawl():
            url = self.member_url.format(**reg)
            print(url)

    def crawl(self):
        ''' Generate a python dict for each registered member in the database.
            Format self.results_rex with this dict for an HTML page possibly containing more
            information including links to filing information.
        '''

        for election_type in ('BA', 'GU', 'PR', 'SP'):
            data = dict(ElectionType     = election_type, 
                        btnSearch        = 'Search',
                        txtCommitteeID   = '',
                        CommitteeType    = '',
                        MemberId         = '',
                        txtCommitteeName = '',
                        hdnAcronymId     = '',
                        txtAcronym       = '',
                        ElectionTypeBA   = '',
                        ddlElectionYear  = '',
                        ddlOfficeType    = '',
                        ddlOfficeSought  = '',
                        ddljurisdiction  = '',
                        dtStartDate      = '',
                        dtEndDate        = '',
                        CommitteeStatus  = '',
                        hdnPersonID      = '',
                        txtResOfficer    = '',
                        btnSearchSearch  = '')

            page = self.lxmlize(self.search_url, 'POST', data=data)
            yield from self.crawl_search_results(page)

    def crawl_search_results(self, page):
        ''' sub-generator for paginating search forms
        '''
        status_text = page.xpath("//div[@class='t-status-text']/text()")[0]
        first, last, total = map(int, self.results_rex.search(status_text).groups())

        for page_id in range(1, total//last+2):
            data = dict(page=page_id, size=last)
            headers = {'origin' : 'https://campaignfinancemd.us', 
                       'referer': self.search_url,
                       'X-Requested-With' : 'XMLHttpRequest'}

            # With these headers, JSON data is returned, which is quite sufficient.
            # The web interface returns an HTML page like the search page, and the links to
            # the individual donor pages could be scraped like:
            # gridresults = page.xpath("//div[@id='GridResults']//a[contains(@href,'ShowReview')]/@href")

            results = self.post(self.committee_url, data=data, headers=headers).json()
            yield from results['data']

