# Copyright (c) Sunlight Foundation, 2014, under the terms of the BSD-3
# license, a copy of which is in the root level LICENSE file.
#   Paul R. Tagliamonte <paultag@sunlightfoundation.com>

from pupa.scrape import Jurisdiction, Post, Organization
from .registrations import MissouriRegistrationScraper


class Missouri(Jurisdiction):
    division_id = 'ocd-division/country:us/state:mo'
    classification = 'government'
    name = "Missouri State Government"
    url = 'http://alaska.gov/'

    scrapers = {
        "regs": MissouriRegistrationScraper
    }

    def get_organizations(self):
        org = Organization(name='Missouri Executive Branch',
                           classification='executive')
        yield org
