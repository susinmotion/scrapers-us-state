from pupa.scrape import Scraper
from utils import LXMLMixin  # XXX: Fixme - need a superpackage.

import csv

SEARCH_URL = "https://aws.state.ak.us/ApocReports/StatementContributions/SCForms.aspx"



class AlaskaContributionsScraper(LXMLMixin, Scraper):

    def scrape(self):
        yield from self.scrape_csv_export()


    def scrape_csv_export(self):
        data = self.lxmlize(SEARCH_URL, 'post')
        data = {
            x.attrib['name']: x.attrib.get('value', None) for x in
                data.xpath("//form[@id='aspnetForm']//input")
        }
        print(data.keys())
        self.post(SEARCH_URL, data=data)

        data = self.get("https://aws.state.ak.us/ApocReports/"
                        "StatementContributions/SCForms.aspx?"
                        "exportAll=True&exportFormat=CSV&isExport=True")
        print(data.content)
