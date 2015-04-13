# Copyright (c) Sunlight Foundation, 2014, under the terms of the BSD-3
# license, a copy of which is in the root level LICENSE file.
#   Paul R. Tagliamonte <paultag@sunlightfoundation.com>

from pupa.scrape import Jurisdiction, Post, Organization
from .people import AlabamaPersonScraper


class Alabama(Jurisdiction):
    division_id = 'ocd-division/country:us/state:al'
    classification = 'government'
    name = "Alabama State Government"
    url = 'http://www.alabama.gov/'

    scrapers = {
        "people": AlabamaPersonScraper
    }

    def get_organizations(self):
        org = Organization(name='Alabama Executive Branch',
                           classification='executive')
        yield org
