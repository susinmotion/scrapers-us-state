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

        # Initialize the Organization class. Use keyword args to set the basic
        # properties.
        secretary_of_state = Organization(
            name="Office of the Secretary of State, State of Arizona",
            classification="office"
        )

        #  
        secretary_of_state.add_contact_detail(
            type="voice",
            value="602-542-4285"
        )

        secretary_of_state.add_contact_detail(
            type="address",
            value="1700 W Washington St Fl 7, Phoenix AZ 85007-2808"
        )
        secretary_of_state.add_link(
            url="http://www.azsos.gov/",
            note="Home page"
        )

        self._secretary_of_state = secretary_of_state

        yield secretary_of_state
