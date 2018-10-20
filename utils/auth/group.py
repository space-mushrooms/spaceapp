from django.contrib.auth.decorators import user_passes_test
from utils.auth.user import get_group_names


def check_group(function=None, group_name=None):
    actual_decorator = user_passes_test(
        lambda u: group_name in get_group_names(u),
        login_url='/auth/error/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def check_groups(function=None, group_names=None):
    def check_any_group_in_list(group_names, list):
        return bool(set(group_names) & set(list))

    actual_decorator = user_passes_test(
        lambda u: check_any_group_in_list(group_names, get_group_names(u)),
        login_url='/auth/error/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
