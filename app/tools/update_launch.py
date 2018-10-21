import os
from datetime import timedelta, datetime

import requests
from django.core.files.storage import default_storage
from django.utils import timezone

from app.models import Launch, SpaceAgency, Rocket
from utils.tools.launchlibrary_api import LaunchLibraryClient, to_datetime


def update_launch():
    api = LaunchLibraryClient()
    now_dt = timezone.now().replace(tzinfo=None)

    statuses_map = {
        1: 'ready',
        2: 'tbd',
        3: 'success',
        4: 'failure',
        5: 'hold',
        6: 'in_flight',
        7: 'partial_failure',
    }
    space_agency_ids = {x.external_id: x.id for x in SpaceAgency.objects.all()}

    launch_data = api.get_list('launch')
    for item in launch_data:

        try:
            launch = Launch.objects.get(external_id=item['id'], external_id__isnull=False)
            if launch.updated_dt and launch.updated_dt.replace(tzinfo=None) <= to_datetime(item['changed']):
                continue

            launch.name = item.get('name')
            launch.window_start_dt = to_datetime(item.get('windowstart'))
            launch.window_close_dt = to_datetime(item.get('windowend'))
            launch.start_dt = to_datetime(item.get('net'), format='%B %d, %Y %H:%M:%S UTC')
            launch.status = statuses_map.get(item.get('status')) or 2
            launch.hold_reason = item.get('holdreason') or None
            launch.failure_reason = item.get('failreason') or None
            launch.hashtag = item.get('hashtag') or None
            launch.space_agency_id = space_agency_ids.get(item.get('lsp')) or None

            launch.updated_dt = now_dt

            update_fields = ['name', 'window_start_dt', 'window_close_dt', 'start_dt', 'status', 'hold_reason',
                             'failure_reason', 'hashtag', 'space_agency_id', 'updated_dt']
            launch.save(update_fields=update_fields)
            print('Updated: {} [{}]'.format(launch.name, launch.external_id))

        except Launch.DoesNotExist:
            launch = Launch.objects.create(
                external_id=item.get('id'),
                name=item.get('name'),
                window_start_dt=to_datetime(item.get('windowstart')),
                window_close_dt=to_datetime(item.get('windowend')),
                start_dt=to_datetime(item.get('net'), format='%B %d, %Y %H:%M:%S UTC'),
                status=statuses_map.get(item.get('status')) or 2,
                hold_reason=item.get('holdreason') or None,
                failure_reason=item.get('failreason') or None,
                hashtag=item.get('hashtag') or None,
                space_agency_id=space_agency_ids.get(item.get('lsp')) or None,
                updated_dt=now_dt,
            )
            print('Created: {} [{}]'.format(launch.name, launch.external_id))

    rocket_ids = {x.external_id: x.id for x in Rocket.objects.all()}
    launches = Launch.objects.filter(
        status__in=[Launch.STATUS_READY, Launch.STATUS_SUCCESS],
        start_dt__gte=datetime.now() - timedelta(days=365*5),
    )
    for item in launches:
        launch_data = api.get_item('launch', id=item.external_id)
        update_fields = []

        if launch_data.get('missions'):
            item.mission = launch_data['missions'][0].get('name')
            item.mission_description = launch_data['missions'][0].get('name')
            update_fields.extend(['mission', 'mission_description'])

        if launch_data.get('rocket'):
            item.rocket_id = rocket_ids.get(launch_data['rocket'].get('id')) or None
            update_fields.append('rocket')

        if launch_data.get('infoURL'):
            item.info_url = launch_data.get('infoURL')
            update_fields.append('info_url')

        if launch_data.get('vidURL'):
            item.stream_url = launch_data.get('vidURL')
            update_fields.append('stream_url')

        item.save(update_fields=update_fields)
        print('Detailed: {} [{}]'.format(item.name, item.external_id))
