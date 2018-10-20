from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class AuthModelBackend(ModelBackend):

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.prefetch_related('groups').get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
