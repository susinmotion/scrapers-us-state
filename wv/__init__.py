# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .people import WvPersonScraper


class Wv(Jurisdiction):
    division_id = "ocd-division/country:us/state:wv"
    classification = "government"
    name = "West Virginia"
    url = "http://www.wv.gov/"
    scrapers = {
        "people": WvPersonScraper,
    }

    def get_organizations(self):
        yield Organization(name=None, classification=None)
