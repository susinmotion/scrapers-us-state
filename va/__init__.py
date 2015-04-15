# encoding=utf-8
from pupa.scrape import Jurisdiction, Organization
from .events import VirginiaEventScraper
from .people import VirginiaPersonScraper
from .disclosures import VirginiaDisclosureScraper


class Virginia(Jurisdiction):
    division_id = "ocd-division/country:us/state:va"
    classification = "government"
    name = "Virginia"
    url = "http://www.virginia.gov/"
    scrapers = {
        "disclosures": VirginiaDisclosureScraper,
        "events": VirginiaEventScraper,
        "people": VirginiaPersonScraper,
    }

    def get_organizations(self):

        secretary_of_the_commonwealth = Organization(
            name="Office of the Secretary of the Commonwealth, Commonwealth of Virginia",
            classification="office"
        )
        secretary_of_the_commonwealth.add_contact_detail(
            type="voice",
            value="804-786-2441"
        )
        secretary_of_the_commonwealth.add_contact_detail(
            type="address",
            value="1111 East Broad Street, 4th Floor, Richmond, Virginia 23219"
        )
        secretary_of_the_commonwealth.add_link(
            url="https://commonwealth.virginia.gov/",
            note="Home page"
        )

        self._secretary_of_the_commonwealth = secretary_of_the_commonwealth

        yield secretary_of_the_commonwealth
