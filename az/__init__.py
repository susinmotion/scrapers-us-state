# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import ArizonaEventScraper
from .people import ArizonaPersonScraper
from .disclosures import ArizonaDisclosureScraper


class Arizona(Jurisdiction):
    division_id = "ocd-division/country:us/state:az"
    classification = "government"
    name = "Arizona"
    url = "https://az.gov/"
    scrapers = {
        "events": ArizonaEventScraper,
        "people": ArizonaPersonScraper,
        "disclosures": ArizonaDisclosureScraper,
    }

    def get_organizations(self):
        yield Organization(name=None, classification=None)
