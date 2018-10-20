import json
import logging

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import RedirectView
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError

from utils.views.base import DefaultView

logger = logging.getLogger('debug')


class RedirectToGoogle(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        google = google_client()
        state = '/'
        next_url = self.request.GET.get('next')
        if next_url:
            state = next_url
        auth_uri = google.step1_get_authorize_url(state=state)
        return auth_uri


class Logout(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logger.debug('{} logged out'.format(self.request.user.email))
            auth.logout(self.request)
        return '/'


class AccessDenied(DefaultView):
    template_name = 'access_denied.html'

    def get(self, request):
        if not request.user.is_anonymous:
            self.get_config(request)
        else:
            next_url = request.GET.get('next')
            if next_url:
                return redirect(settings.LOGIN_URL + '?next=' + next_url)

        self.args = {'email': request.GET.get('email')}
        return render(request, self.template_name, self.args)


class Login(DefaultView):
    template_name = 'login.html'

    def get(self, request):
        if request.GET.get('code'):
            return google_login(request)

        next_url = self.request.GET.get('next')
        self.args = {'user_has_access': False, 'next_url': next_url}
        return render(request, self.template_name, self.args)


def google_client():
    """
    Создание клиента подключения к Google
    """
    auth = settings.GOOGLE_AUTH
    google = OAuth2WebServerFlow(
        client_id=auth.get('client_id'),
        client_secret=auth.get('client_secret'),
        scope='https://www.googleapis.com/auth/userinfo.email',
        redirect_uri=auth.get('redirect_url'),
    )
    return google


def google_login(request):
    """
    Авторизация пользователя на основе присланных данных из Google
    """
    if request.GET.get('error'):
        return redirect(settings.ACCESS_DENIED_URL)

    google = google_client()

    # Получаем code авторизации от Google
    code = request.GET.get('code')
    next_url = request.GET.get('state')

    # Получаем по code объект с результатом авторизации
    try:
        credentials = google.step2_exchange(code)
    except FlowExchangeError:
        logging.error('Something happened with google auth', extra={'stack': True})
        return redirect(settings.ACCESS_DENIED_URL)

    data = credentials.to_json()

    # Получаем адрес авторизовавшегося пользователя
    email = json.loads(data).get('id_token').get('email')
    access_denied_url = '{}?email={}'.format(settings.ACCESS_DENIED_URL, email)
    if email:
        user = User.objects.filter(email=email.lower()).last()
        if user and user.is_active:
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
            # Авторизуем пользователя
            auth.login(request, user)
            logger.debug('{} logged in'.format(request.user.email))
            return redirect(next_url)

    return redirect(access_denied_url)
