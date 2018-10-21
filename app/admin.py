import binascii
import os

from django import forms
from django.contrib import admin

from app.models import *


# class ApiAccessForm(forms.ModelForm):
#     service = forms.CharField(widget=forms.TextInput, required=True)
#     description = forms.CharField(widget=forms.Textarea, required=False)
#
#     class Meta:
#         model = ApiAccess
#         fields = ('service', 'token', 'description')
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # generate new token when create new one
#         self.fields['token'].initial = binascii.hexlify(os.urandom(20)).decode()
#
#
# class ApiAccessAdmin(admin.ModelAdmin):
#     search_fields = ['service']
#     list_display = ['service', 'token', 'description']
#     ordering = ['service']
#     form = ApiAccessForm
#
#
# admin.site.register(ApiAccess, ApiAccessAdmin)


@admin.register(Launch)
class LaunchAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'start_dt', 'status', 'rocket']
    ordering = ['start_dt']
    list_filter = ['status']


@admin.register(Rocket)
class RocketAdmin(admin.ModelAdmin):
    search_fields = ['name', 'family']
    list_display = ['name', 'family', 'description', 'image']
    ordering = ['name']


@admin.register(SpaceAgency)
class SpaceAgencyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    ordering = ['name']


@admin.register(SpacePort)
class SpacePortAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    ordering = ['name']


@admin.register(Astronaut)
class AstronautAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    ordering = ['name']


@admin.register(RocketPad)
class RocketPadAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']
    ordering = ['name']
