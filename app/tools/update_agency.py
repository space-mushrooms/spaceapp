from django.utils import timezone

from app.models import SpaceAgency
from utils.tools.launchlibrary_api import LaunchLibraryClient, to_datetime


def update_agency():
    api = LaunchLibraryClient()
    now_dt = timezone.now().replace(tzinfo=None)

    agency_type_data = api.get_list('agencytype')
    agency_type_ids = {x.get('id'): x.get('name') for x in agency_type_data}

    agency_data = api.get_list('agency')
    for item in agency_data:

        try:
            agency = SpaceAgency.objects.get(external_id=item['id'], external_id__isnull=False)
            if agency.updated_dt and agency.updated_dt.replace(tzinfo=None) <= to_datetime(item['changed']):
                continue

            agency.abbrev = item.get('name')
            agency.abbrev = item.get('abbrev')
            agency.country_code = item.get('countryCode')
            agency.type = agency_type_ids.get(item.get('type')) or SpaceAgency.TYPE_UNKNOWN
            agency.website_url = item.get('infoURL')
            agency.wiki_url = item.get('wikiURL')
            agency.is_lsp = item.get('islsp') or False
            agency.updated_dt = now_dt

            update_fields = ['abbrev', 'country_code', 'type', 'website_url', 'wiki_url', 'is_lsp', 'updated_dt']
            agency.save(update_fields=update_fields)
            print('Updated: {} [{}]'.format(agency.name, agency.external_id))

        except SpaceAgency.DoesNotExist:
            agency = SpaceAgency.objects.create(
                external_id=item.get('id'),
                name=item.get('name'),
                abbrev=item.get('abbrev'),
                country_code=item.get('countryCode'),
                type=agency_type_ids.get(item.get('type')) or SpaceAgency.TYPE_UNKNOWN,
                website_url=item.get('infoURL'),
                wiki_url=item.get('wikiURL'),
                is_lsp=item.get('islsp') or False,
                updated_dt=now_dt,
            )
            print('Created: {} [{}]'.format(agency.name, agency.external_id))
