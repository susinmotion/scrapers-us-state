from pupa.scrape import Scraper
from pupa.scrape import Disclosure
from pupa.scrape.popolo import Organization
from lxml import etree
from lxml.html import HTMLParser
import scrapelib
#from datetime import datetime

class VirginiaDisclosureScraper(Scraper):

    def scrape_committees(self):
        SEARCH_COMMITTEES_URL="http://cfreports.sbe.virginia.gov/"
        my_scraper = scrapelib.Scraper()
        _, resp = my_scraper.urlretrieve(SEARCH_COMMITTEES_URL)
        d = etree.fromstring(resp.content, parser=HTMLParser())
        number_of_result_pages=int(d.xpath('//span[@id="PagingTotalPages"]/text()')[0])

        target_table = d.xpath('//table/tbody')[0]
        scraped_rows = []
        for row in target_table.xpath('tr'):
            data_dict = {}
            columns = row.xpath('td')
            name = columns[0].text_content().strip()
            if not (name == ""):
                data_dict['org_name'] = name
                scraped_rows.append(data_dict)

        for result in scraped_rows:

            org = Organization(
                name=result['org_name'],
                classification='political action committee',
            )
            org.add_source(url=SEARCH_COMMITTEES_URL)
            org.source_identified = True
            yield org 

    def scrape(self):
        yield from self.scrape_committees()
