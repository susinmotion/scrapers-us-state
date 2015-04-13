from pupa.scrape import Scraper, Person, Membership
from ..utils.lxmlize import LXMLMixin

class MarylandRegistrationScraper(Scraper, LXMLMixin):
    ''' https://campaignfinancemd.us/Public/ViewCommittees
    '''

    url = 'https://campaignfinancemd.us/Public/Search?theme=vista'

    def scrape(self):
        pass

    def crawl(self):
        ''' generate URLs to scrape
        '''

        for election_types ('BA', 'GU', 'PR', 'SP'):
            data = dict( ElectionType = committee_type, 
                         btnSearch = Search )
            resp = self.post(self.url, data=data)
            r.raise_for_status()

