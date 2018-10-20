import json

from django.http import JsonResponse

from utils.auth.user import get_group_names
from utils.views.base import GroupRequiredMixin, DefaultView


class JsonView(GroupRequiredMixin, DefaultView):
    response = {'status': 'error', 'error_message': 'Bad request'}

    def get(self, request, *args, **kwargs):
        self.get_config(self.request)

        if not self.check_rights():
            return JsonResponse({'status': 'error', 'error_message': 'You are not allowed for this action'})

        request_body = request.GET.copy()
        self.response = self.get_logic(request_body)

        return JsonResponse(self.response)

    def post(self, request, *args, **kwargs):
        self.get_config(self.request)

        if not self.check_rights():
            return JsonResponse({'status': 'error', 'error_message': 'You are not allowed for this action'})

        request_body = json.loads(self.request.body.decode())
        self.response = self.get_logic(request_body)

        return JsonResponse(self.response)

    def get_logic(self, data):
        response = {'status': 'error', 'error_message': 'Method not implemented'}
        return response

    def check_rights(self):
        return set(self.groups) & set(get_group_names(self.request.user))
