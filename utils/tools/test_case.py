import json
import random
import string

from django.urls import reverse

import settings
import datetime as dt

from decimal import Decimal, ROUND_UP

from django.contrib.auth.models import User, Group
from django.test import TestCase

from apps.services.models.leave import Leave, LeaveReplacer
from apps.services.models.questionnaire import RecruitQuestionnaireField
from apps.users.models.company import Company
from apps.users.models.location import Location
from apps.users.models.profile import Profile
from apps.users.models.team import Team


class FakeResponse:
    content = {}
    status_code = 200

    def __init__(self, content, status_code=200):
        self.content = content
        self.status_code = status_code

    def raise_for_status(self):
        pass


class DefaultTestCase(TestCase):
    date_format = '%d.%m.%Y'  # 31.12.2016
    datetime_format = '%d.%m.%Y %H:%M'  # 31.12.2016 15:59

    CONTENT_TYPE_JSON = 'application/json'

    def setUp_test(self):
        pass

    def gen_random_text(self, limit=10):
        """
        :type limit: int
        :rtype: core_basestring
        """
        letters = string.digits + string.ascii_letters
        random_text = ''.join(random.choice(letters) for _ in range(limit))
        return random_text

    def gen_random_email(self):
        """
        :rtype: core_basestring
        """
        return '{0}@{0}.com'.format(self.gen_random_text())

    def gen_random_date(self):
        """
        :rtype: dt_date
        """
        return self.gen_random_datetime().date()

    def gen_random_date_text(self):
        """
        :rtype: core_basestring
        """
        return self.gen_random_date().strftime(self.date_format)

    def gen_random_time(self):
        """
        :rtype: dt_date
        """
        return self.gen_random_datetime().time()

    def gen_random_datetime(self):
        """
        :rtype: dt_datetime
        """
        # ATTENTION!
        # typeddict .simplify() precision loose seconds, so we must generate always 0 seconds
        return dt.datetime.fromtimestamp(random.randint(1, 9999999999)).replace(second=0)

    def gen_random_datetime_text(self):
        """
        :rtype: core_basestring
        """
        return self.gen_random_datetime().strftime(self.datetime_format)

    def gen_random_bool(self):
        """
        :rtype: bool
        """
        return random.choice((True, False))

    def gen_random_decimal(self, to=999999):
        """
        :rtype: Decimal
        """
        return Decimal(random.randrange(-to, to)) / Decimal('100').quantize(Decimal('.01'), ROUND_UP)

    def gen_random_positive_decimal(self, to=999999):
        """
        :rtype: Decimal
        """
        return Decimal(random.randrange(1, to)) / Decimal('100').quantize(Decimal('.01'), ROUND_UP)

    def gen_random_decimal_str(self, to=999999):
        """
        :rtype: str
        """
        return str(self.gen_random_positive_decimal(to))

    def gen_random_int(self, to=1000):
        """
        :rtype: int
        """
        return random.randint(-to, to)

    def gen_random_positive_int(self, to=1000):
        """
        :rtype: int
        """
        return abs(self.gen_random_int(to)) + 1

    def gen_random_choice(self, choices, exclude=None):
        """
        :rtype: core_basestring
        """
        choice = random.choice([c for c in choices if c not in (exclude or [])])
        return choice[0] if isinstance(choice, (list, tuple)) else choice


class BaseTestCase(DefaultTestCase):
    def setUp(self):
        # Users
        self.user1 = self.gen_random_user(groups=['HR manager', 'Read'])

        self.company = self.create_user_company(self.user1)
        self.location = self.create_user_location(self.user1)
        self.team = self.create_user_team()

        # Urls
        self.profile_url_save = reverse('team:profile_add_save')
        self.profile_fire_request = reverse('team:profile_fire_request')

        # profile access
        self.profile_access_activate = reverse('team:profile_access_item_activate')
        self.profile_access_deactivate = reverse('team:profile_access_item_deactivate')

        # leave system
        self.profile_leave_create = reverse('team:leave_save')
        self.profile_leave_replacer_request = reverse('team:leave_replacer_request')

    def fake_sync_before_update(self):
        return True

    def fake_run_task(self, *args, **kwargs):
        return

    def gen_random_profile_data(self, date_to_string=False, **kwargs):
        return {
            'last_name_original': self.gen_random_text(),
            'first_name_original': self.gen_random_text(),
            'last_name': self.gen_random_text(),
            'first_name': self.gen_random_text(),
            'gender': self.gen_random_choice(Profile.GENDER_CHOICES),
            'email': self.gen_random_email(),
            'birthday': self.gen_random_date() if not date_to_string else self.gen_random_date_text(),
            'mobile_phone': str(self.gen_random_positive_int()),
            'email_personal': self.gen_random_email(),
            'position': self.gen_random_text(),
            'work_type': self.gen_random_choice(Profile.WORK_TYPE_CHOICES),
            'work_date_start': self.gen_random_date() if not date_to_string else self.gen_random_date_text(),
            'brand': self.gen_random_choice(Profile.BRAND_CHOICES),
            'slack_user_id': self.gen_random_text(),
            **kwargs,
        }

    def gen_random_user(self, email=None, password='test', groups=None):
        user = User.objects.create_user(
            username=self.gen_random_text(),
            first_name=self.gen_random_text(),
            last_name=self.gen_random_text(),
            password=password or self.gen_random_text(),
            email=email or self.gen_random_email(),
        )

        profile_data = self.gen_random_profile_data(
            user_id=user.pk,
            location=self.create_user_location(user), team=self.create_user_team(),
            company=self.create_user_company(user), created_by_id=user.pk, modified_by_id=user.pk
        )
        Profile.objects.create(**profile_data)

        _groups = []
        for name in groups or []:
            group, created = Group.objects.get_or_create(name=name)
            _groups.append(group)
        user.groups.add(*_groups)
        return user

    def auth_user(self, user=None, password='test'):
        if user is None:
            user = self.gen_random_user()
        self.client.logout()
        authorize = self.client.login(username=user.username, password=password)
        self.assertTrue(authorize)
        return user

    def assertEqualDatetime(self, dt1, dt2):
        """
        :type dt1: dt_datetime
        :type dt2: dt_datetime
        :rtype: None
        """
        import pytz
        if isinstance(dt1, dt.datetime) and not dt1.tzinfo:
            dt1 = dt1.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

        if dt2.tzinfo is None:
            dt2 = dt2.replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

        self.assertEqual(
            dt1.strftime('%Y-%m-%d %H:%M:%S'),
            dt2.strftime('%Y-%m-%d %H:%M:%S'),
        )

    def assertEqualObjectDict(self, obj, dict_, **kwargs):
        for key, value in {**dict_, **kwargs}.items():
            if not hasattr(obj, key):
                continue
            attr_key = getattr(obj, key)
            if isinstance(attr_key, dt.datetime):
                self.assertEqual(attr_key.strftime(self.datetime_format), value)
            elif isinstance(attr_key, dt.date):
                self.assertEqual(attr_key.strftime(self.date_format), value)
            elif isinstance(attr_key, Decimal):
                self.assertEqual(str(attr_key), str(Decimal(value).quantize(Decimal('.01'))))
            elif attr_key is None:
                self.assertIn(value, (None, ''))
            else:
                self.assertEqual(attr_key, value)

    def assertResponseJSON(self, response, status_code=200, json_status='success'):
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response['Content-Type'], 'application/json')
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_data['status'], json_status)
        return response_data

    def create_user_team(self):
        return Team.objects.create(**{
            'name': self.gen_random_text(),
            'name_original': self.gen_random_text(),
            'level': self.gen_random_int(),
            'sort': self.gen_random_int(),
            'team_uid': self.gen_random_int()
        })

    def create_user_company(self, user):
        return Company.objects.create(**{
            'slug': self.gen_random_text(),
            'name': self.gen_random_text(),
            'name_original': self.gen_random_text(),
            'created_by': user,
            'modified_by': user
        })

    def create_user_location(self, user):
        return Location.objects.create(**{
            'name': self.gen_random_text(),
            'location_type': self.gen_random_choice(Location.LOCATION_TYPE_CHOICES),
            'created_by': user,
            'modified_by': user
        })

    def create_dummy_profile(self):
        profile_data = self.gen_random_profile_data(
            location=self.location,
            team=self.team, company=self.company,
            created_by=self.user1, modified_by=self.user1
        )
        return Profile.objects.create(**profile_data)

    def create_dummy_leave(self, profile):
        leave_data = {
            'profile': profile,
            'leave_type': self.gen_random_choice(Leave.LEAVE_TYPE_CHOICES),
            'date_start': self.gen_random_date(),
            'date_end': self.gen_random_date(),
            'comment': self.gen_random_text(),
            'created_by': self.user1,
            'modified_by': self.user1,
        }
        return Leave.objects.create(**leave_data)

    def create_dummy_leave_replacer(self, leave, replacer, status=None):
        replacer_data = {
            'leave': leave,
            'profile': replacer,
            'comment': self.gen_random_text(),
            'status': status,
            'created_by': self.user1,
            'modified_by': self.user1,
        }
        return LeaveReplacer.objects.create(**replacer_data)

    def create_dummy_recruit_question(self, has_answers=True):
        answers = [self.gen_random_text() for i in range(self.gen_random_positive_int(5))] if has_answers else []

        return RecruitQuestionnaireField.objects.create(
            question=self.gen_random_text(),
            slug=self.gen_random_text(),
            answers=answers,
            is_active=True,
            has_comment_field=True,
            created_by=self.user1,
            modified_by=self.user1
        )
