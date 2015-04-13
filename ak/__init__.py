# Copyright (c) Sunlight Foundation, 2014, under the terms of the BSD-3
# license, a copy of which is in the root level LICENSE file.
#   Paul R. Tagliamonte <paultag@sunlightfoundation.com>

from pupa.scrape import Jurisdiction, Post, Organization
from .contributions import AlaskaContributionsScraper


class Alaska(Jurisdiction):
    division_id = 'ocd-division/country:us/state:ak'
    classification = 'government'
    name = "Alaska State Government"
    url = 'http://alaska.gov/'

    scrapers = {
        "contributions": AlaskaContributionsScraper
    }

    def get_organizations(self):
        org = Organization(name='Alabama Executive Branch',
                           classification='executive')
        yield org
