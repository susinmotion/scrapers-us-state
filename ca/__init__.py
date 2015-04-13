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
        secretary_of_state = Organization(                                    
            name="Office of the Secretary of State, State of California",        
            classification="office"                                           
        )

        secretary_of_state.add_contact_detail(                                
            type="voice",                                                     
            value="916-653-6814"
        )                    

        secretary_of_state.add_contact_detail(                                
            type="address",                                                   
            value="1500 11th Street, Sacramento, CA 95814"
        )
                                                                     
        secretary_of_state.add_link(                                          
            url="http://www.sos.ca.gov",                                      
            note="Home page"                                                  
        )

        self._secretary_of_state = secretary_of_state
        yield secretary_of_state
