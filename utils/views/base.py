from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View

from utils.auth.group import check_groups
from utils.auth.user import get_group_names


def get_form_errors(form):
    return {field: str(form.errors[field][0])
            for field in form.fields if form.has_error(field)}


class DefaultView(View):
    """
    Method get_config initiate args['user'] and config
    """
    args, config = {}, {}

    @method_decorator(login_required)
    def get_config(self, request):
        profile = request.user.profile
        self.args = {'user': request.user, 'groups': get_group_names(request.user)}

    def dispatch(self, request, *args, **kwargs):
        self.get_config(request)
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required(view)


class GroupRequiredMixin(LoginRequiredMixin):
    """
    Check user is authenticate and has groups
    """
    groups = None

    @classmethod
    def as_view(cls, **initkwargs):
        if cls.groups is None:
            raise NotImplementedError
        view = super().as_view(**initkwargs)
        return check_groups(view, cls.groups)
