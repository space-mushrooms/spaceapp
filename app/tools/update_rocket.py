import os

import requests
from django.core.files.storage import default_storage
from django.utils import timezone

from app.models import Rocket
from utils.tools.launchlibrary_api import LaunchLibraryClient, to_datetime


def update_rocket():
    api = LaunchLibraryClient()
    now_dt = timezone.now().replace(tzinfo=None)

    rockets_data = api.get_list('rocket')
    for item in rockets_data:

        family = None
        manufacturer = None
        if item.get('family'):
            family = item['family'].get('name')
            manufacturer = item['family'].get('agencies').split(',')[0] if item.get('agencies') else None

        try:
            rocket = Rocket.objects.get(external_id=item['id'], external_id__isnull=False)
            # if rocket.updated_dt and rocket.updated_dt.replace(tzinfo=None) <= to_datetime(item['changed']):
            #     continue

            rocket.name = item.get('name')
            rocket.configuration = item.get('configuration')
            rocket.family = family
            rocket.manufacturer_id = manufacturer
            rocket.wiki_url = item.get('wikiURL'),
            rocket.updated_dt = now_dt

            update_fields = ['name', 'configuration', 'family', 'manufacturer', 'wiki_url', 'image', 'updated_dt']
            rocket.save(update_fields=update_fields)
            print('Updated: {} [{}]'.format(rocket.name, rocket.external_id))

        except Rocket.DoesNotExist:
            rocket = Rocket.objects.create(
                external_id=item.get('id'),
                name=item.get('name'),
                configuration=item.get('configuration'),
                family=family,
                manufacturer_id=manufacturer,
                wiki_url=item.get('wikiURL'),
                updated_dt=now_dt,
            )
            print('Created: {} [{}]'.format(rocket.name, rocket.external_id))

        if not rocket.image and item.get('imageURL'):
            image_url = item.get('imageURL')
            response = requests.get(image_url)
            file_temporary_url = os.path.join('tmp', os.path.basename(image_url))
            with default_storage.open(file_temporary_url, 'wb') as f:
                f.write(response.content)
            with default_storage.open(file_temporary_url) as f:
                rocket.image.save(os.path.basename(image_url), f)
            rocket.save()
