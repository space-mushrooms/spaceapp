import ujson

from collections import OrderedDict

import urllib3
import logging
import requests

from redis import StrictRedis
from requests.exceptions import RequestException


class BaseApiException(Exception):
    pass


class MethodIsNotDefined(BaseApiException):
    pass


class ServiceDoesNotExist(BaseApiException):
    pass


class CustomField:
    def __init__(self, name, label, value=None, field_type='checkbox', choices=None, readonly=False):
        self.name = name
        self.label = label
        self.value = value
        self.field_type = field_type
        self.choices = choices
        self.readonly = readonly

    def as_dict(self):
        choices = OrderedDict()
        if isinstance(self.choices, list) and self.field_type == 'checkbox':
            for choice in self.choices:
                choices[choice] = choice
        return {
            'name': self.name,
            'label': self.label,
            'value': self.value,
            'field_type': self.field_type,
            'choices': choices or self.choices,
            'readonly': self.readonly
        }


class BaseApiMeta(type):
    sort = 100

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if cls.service_name:
            if cls.service_name in cls.registry:
                raise KeyError('Service {} already registered'.format(cls.service_name))
            cls.registry[cls.service_name] = cls
        return cls


class BaseResponse:
    STATUS_SUCCESS = 'success'
    STATUS_ERROR = 'error'

    def __init__(self, status, code, response=None, error_message=None):
        self.status = status
        self.code = code
        self.response = response
        self.error_message = error_message

    @property
    def is_ok(self):
        """
        :rtype: bool
        """
        return self.status == self.STATUS_SUCCESS

    @property
    def content(self):
        """
        :rtype: dict|str
        """
        if self.response:
            try:
                return ujson.loads(self.response)
            except (TypeError, ValueError):
                return self.response

    @property
    def context(self):
        """
        :rtype: dict
        """
        return {
            'code': self.code,
            'status': self.status,
            'content': self.content,
            'error_message': self.error_message
        }


class BaseApiClient(metaclass=BaseApiMeta):
    service_name = None
    display_name = None

    host = None
    user = None
    password = None
    token = None
    is_internal_service = True

    default_timeout = 3

    authorize_method = 'token'
    authorize_token_field = 'token'
    content_type = 'application/x-www-form-urlencoded'

    registry = {}
    exclude_from_acs = False  # if True remove service from access control system

    JSON_CONTENT_TYPE = 'application/json'

    @classmethod
    def make_service(cls, service_name):
        try:
            return cls.registry[service_name]()
        except KeyError:
            raise ServiceDoesNotExist

    @classmethod
    def get_all_services(cls):
        return [
            service_api() for service_api in sorted(cls.registry.values(), key=lambda _class: _class.sort)
            if not service_api.exclude_from_acs
        ]

    @classmethod
    def get_internal_objects(cls):
        for _class in cls.registry.values():
            if _class.is_internal_service:
                yield _class

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def pre_route_logic(self, request_data):
        if self.authorize_method:
            if self.authorize_method == 'credentials':
                request_data['auth'] = (self.user, self.password)
            else:
                if not request_data['data'] or isinstance(request_data['data'], dict):
                    request_data['data'][self.authorize_token_field] = self.token
                elif isinstance(request_data['data'], list):
                    request_data['data'].append((self.authorize_token_field, self.token))

    def post_route_logic(self, request_data):
        pass

    def get_headers(self):
        return {
            'Content-type': self.content_type,
            'User-Agent': 'intranet "Intranet; https://gitlab.ostrovok.ru/ostrovok/intranet"'
        }

    def request(self, url_path=None, method='GET', direct_url=None, data=None, timeout=None):
        """
        :type url_path: str
        :type method: str
        :type direct_url: str
        :type data: dict|list
        :type timeout: int
        :rtype: BaseResponse
        """
        if not self.host:
            raise ValueError('API host must be specified')

        url = direct_url or '{}{}'.format(self.host, '' or url_path)

        request_data = {
            'headers': self.get_headers(),
            'verify': False,
            'data': data or {},
            'timeout': timeout or self.default_timeout,
        }

        self.pre_route_logic(request_data)

        if method in ['POST', 'PUT', 'PATCH'] and request_data['data'] and self.content_type == self.JSON_CONTENT_TYPE:
            request_data['data'] = ujson.dumps(request_data['data'])
        if method == 'GET' and request_data['data']:
            request_data['params'] = request_data.pop('data')

        self.post_route_logic(request_data)

        try:
            urllib3.disable_warnings()
            resp = requests.request(method, url, **request_data)
            resp.raise_for_status()
        except RequestException as error:
            logging.error('Host {} return status_code = {} for data {}'.format(
                self.host, error.response.status_code if hasattr(error.response, 'status_code') else None, request_data
            ), extra={'stack': True})
            return BaseResponse(
                status=BaseResponse.STATUS_ERROR, code=error.response.status_code if hasattr(error.response, 'status_code') else None,
                error_message=self.get_error_message(error)
            )
        except requests.ReadTimeout:
            return BaseResponse(status=BaseResponse.STATUS_ERROR, code=408, error_message='Request timeout')
        return self.success_response_handler(
            BaseResponse(status=BaseResponse.STATUS_SUCCESS, code=resp.status_code, response=resp.content)
        )

    def get_access_item(self, access_set):
        return access_set.get(self.service_name)

    def get_error_message(self, error):
        return 'Connection error'

    def success_response_handler(self, obj):
        return obj

    def activate(self, data):
        raise MethodIsNotDefined('Method is not allowed for this service')

    def deactivate(self, data):
        raise MethodIsNotDefined('Method is not allowed for this service')

    def sync(self, profile):
        raise MethodIsNotDefined('Method is not allowed for this service')

    def options(self, profile, access_dict):
        pass


class BaseAccessControlAPI(BaseApiClient):
    """
    Base class for accounts access control in Ostrovok.ru services
    """
    urls = {
        'get_groups_list': '/api/intranet/group/',
        'get_users_list': '/api/intranet/user/',
        'get_user': '/api/intranet/user/',
        'update_user': '/api/intranet/user/',
    }

    def get_groups(self):
        url = self.urls.get('get_groups_list')
        return self.request(url)

    def get_users_list(self):
        url = self.urls['get_users_list']
        return self.request(url)

    def get_user(self, email):
        url = self.urls['get_user']
        return self.request(url, data={'email': email})

    def update_user(self, groups, profile, is_active=False):
        url = self.urls['update_user']
        if not is_active:
            groups = []
        return self.request(url, method='POST', data={
            'email': profile.email,
            'groups': groups,
            'is_active': is_active,
            'username': profile.user.username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
        })

    def options(self, profile, access_dict):
        class_fields = []

        redis_groups = StrictRedis().get(self.service_name)
        try:
            group_choices = ujson.loads(redis_groups).get('groups') if redis_groups else []
        except (ValueError, AttributeError):
            group_choices = []

        if not group_choices:
            service_groups = self.get_groups()
            if not service_groups.is_ok:
                return class_fields

            group_choices = service_groups.content
            StrictRedis().set(self.service_name, ujson.dumps({'groups': group_choices}))

        access = self.get_access_item(access_dict)

        try:
            is_active = access.enabled
            group_value = []
            if isinstance(access.options, dict) and access.options.get('groups'):
                group_value = [group for group in access.options['groups']]
        except AttributeError:
            is_active = False
            group_value = []

        class_fields.extend([
            CustomField(name='is_active', label='Access active', value=is_active).as_dict(),
            CustomField(
                name='groups', label='Access Groups',
                value=group_value,
                choices=sorted([group for group in group_choices])
            ).as_dict(),
        ])
        return {'is_active': is_active, 'fields': class_fields}
