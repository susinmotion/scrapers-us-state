from pupa.scrape import Scraper, Organization
from utils import LXMLMixin  # XXX: Fixme - need a superpackage.

import csv
import io

SEARCH_URL = "https://aws.state.ak.us/ApocReports/StatementContributions/SCForms.aspx"



class AlaskaContributionsScraper(LXMLMixin, Scraper):

    def scrape(self):
        yield from self.scrape_csv(csv.DictReader(open(
            'SC_Forms_15-5_04-13-2015.CSV', 'r'
        )))
        # yield from self.scrape_csv_export()


    def scrape_csv_export(self):
        data = self.lxmlize(SEARCH_URL, 'post')
        data = {x.attrib['name']: x.attrib.get('value', None) for x in
                    data.xpath("//form[@id='aspnetForm']//input")}
        response = self.post(SEARCH_URL, data=data)

        data = self.get("https://aws.state.ak.us/ApocReports/"
                        "StatementContributions/SCForms.aspx?"
                        "exportAll=True&exportFormat=CSV&isExport=True")

        yield from self.scrape_csv(csv.DictReader(io.StringIO(data.text)))


    def scrape_csv(self, reader):
        for row in reader:
            print(row)
