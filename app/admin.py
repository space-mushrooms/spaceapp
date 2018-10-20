import binascii
import os

from django import forms
from django.contrib import admin

from app.models.api import ApiAccess


class ApiAccessForm(forms.ModelForm):
    service = forms.CharField(widget=forms.TextInput, required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = ApiAccess
        fields = ('service', 'token', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # generate new token when create new one
        self.fields['token'].initial = binascii.hexlify(os.urandom(20)).decode()


class ApiAccessAdmin(admin.ModelAdmin):
    search_fields = ['service']
    list_display = ['service', 'token', 'description']
    ordering = ['service']
    form = ApiAccessForm


admin.site.register(ApiAccess, ApiAccessAdmin)
