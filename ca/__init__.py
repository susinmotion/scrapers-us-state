# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .disclosures import CaliforniaDisclosureScraper


class California(Jurisdiction):
    division_id = "ocd-division/country:us/state:ca"
    classification = "government"
    name = "California"
    url = "http://www.ca.gov"
    scrapers = {
        "disclosures": CaliforniaDisclosureScraper,
    }

    def get_organizations(self):
        yield Organization(name=None, classification=None)
