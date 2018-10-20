from django import forms
from django.db import models


class DefaultModelForm(forms.ModelForm):
    date_input_formats = ['%d.%m.%Y', '%d.%m.%Y %H:%M']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        _meta = getattr(self, '_meta')
        fields = _meta.fields or {field.name for field in _meta.model._meta.get_fields()}
        exclude_fields = _meta.exclude or set()
        model_fields = {field.name: field for field in _meta.model._meta.get_fields()}

        for field in set(fields) - set(exclude_fields):
            if isinstance(model_fields.get(field), models.DateField):
                self.fields[field].input_formats = self.date_input_formats
