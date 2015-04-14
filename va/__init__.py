# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .disclosures import VirginiaDisclosureScraper
from .bills import VirginiaBillScraper
from .events import VirginiaEventScraper


class Virginia(Jurisdiction):
    division_id = "va"
    classification = "government"
    name = "Virginia"
    url = "http://www.virginia.gov/"
    scrapers = {
        "disclosures": VirginiaDisclosureScraper,
        "bills": VirginiaBillScraper,
        "events": VirginiaEventScraper,
    }

    def get_organizations(self):
        yield Organization(name=None, classification=None)
