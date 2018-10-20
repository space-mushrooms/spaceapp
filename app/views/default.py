from utils.views.view_api import ApiView


class DefaultView(ApiView):
    methods = ['get']

    def get_logic(self, request, data):
        data = []
        self.response = {'status': 200, 'data': data}
