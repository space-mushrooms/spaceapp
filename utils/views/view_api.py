import base64
import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from api.models import ApiAccess


class ApiView(View):
    methods = []
    response_type = 'json'
    authorization_required = False

    format_dt = '%Y-%m-%d %H:%M:%S'
    format_date = '%Y-%m-%d'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response = {'status': 400, 'error': 'Bad request'}
        self.safe = True

    def is_authorized(self, request):
        tokens = ApiAccess.objects.filter().values_list('token', flat=True)
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    decoded_value = base64.b64decode(auth[1]).decode('utf-8')
                    _, auth_token = decoded_value.split(':')
                    if auth_token in tokens:
                        return True
        else:
            auth_token = request.GET.get('token')
            if auth_token and auth_token in tokens:
                return True

        return False

    def get(self, request):
        if 'get' not in self.methods:
            raise NotImplementedError('This method is not allowed')

        if self.response is None:
            raise NotImplementedError('Error response must be specified')

        if self.authorization_required and not self.is_authorized(request):
            self.response = {'status': 403, 'error': 'Forbidden, authorization is required'}
        else:
            data = request.GET.copy()
            self.get_logic(request, data)

        if self.response_type == 'redirect':
            return HttpResponseRedirect(self.response)
        elif self.response_type == 'http':
            return HttpResponse(self.response, content_type="application/json")
        else:
            return JsonResponse(self.response, safe=self.safe)

    def post(self, request):
        """
        Works only with json data (json.loads(request.body))
        """
        if 'post' not in self.methods:
            raise NotImplementedError('This method is not allowed')

        if self.response is None:
            raise NotImplementedError('Error response must be specified')

        if self.authorization_required and not self.is_authorized(request):
            self.response = {'status': 403, 'error': 'Forbidden, authorization is required'}
        else:
            post_data = json.loads(request.body.decode())
            self.post_logic(request, post_data)

        return JsonResponse(self.response, safe=self.safe)

    def get_logic(self, request, data):
        raise NotImplementedError

    def post_logic(self, request, data):
        raise NotImplementedError
