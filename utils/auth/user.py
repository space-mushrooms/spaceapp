from django.contrib.auth.models import Group
from django.db import ProgrammingError

#  Default groups
CUSTOM_GROUPS = [
    'Read',  # Standard group for read all public pages
]

try:
    _existing_groups = Group.objects.values_list('name', flat=True)
    # default groups
    for name in set(CUSTOM_GROUPS) - set(_existing_groups):
        Group.objects.get_or_create(name=name)

except ProgrammingError:
    print('Warning: Default database objects are not initialized')


def get_group_names(user):
    if user.is_superuser:
        return CUSTOM_GROUPS
    return [g.name for g in user.groups.all()]


def user_context(request):
    user_groups = []

    user = request.user

    if user.is_authenticated:
        user_groups = get_group_names(user)

    result = {'groups': user_groups}

    return result
