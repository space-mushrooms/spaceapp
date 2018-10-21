from datetime import datetime, timedelta

from django.forms import model_to_dict

from app.models import Launch
from utils.views.view_api import ApiView


class DefaultView(ApiView):
    methods = ['get']

    def get_logic(self, request, data):
        data = []
        self.response = {'status': 200, 'data': data}


class LaunchView(ApiView):
    methods = ['get']

    def get_logic(self, request, data):
        filter = data.get('filter')
        limit = 30

        params = {}
        if filter == 'upcoming':
            params = {
                'start_dt__gte': datetime.now() - timedelta(days=1),
                'status__in': ['tbd', 'ready', 'in_flight', 'hold'],
            }
            limit = 3

        data = []
        items = Launch.objects.select_related('rocket', 'rocket_pad', 'space_agency').filter(**params).order_by('start_dt')[:limit]
        for item in items:
            obj = model_to_dict(item, fields=[field.name for field in item._meta.fields if field.name != 'image'])
            if item.rocket:
                obj['rocket'] = model_to_dict(item.rocket, fields=[field.name for field in item.rocket._meta.fields if field.name != 'image'])

            if item.rocket:
                obj['space_agency'] = model_to_dict(item.space_agency, fields=[field.name for field in item.space_agency._meta.fields if field.name != 'logo'])
            data.append(obj)

        self.response = {'status': 200, 'data': data}
