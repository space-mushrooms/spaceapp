from django.utils import timezone
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.filters import RelatedFieldListFilter


class DateFieldFilter(DateFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_until = '%s__lt' % field_path

        now = timezone.now()

        if timezone.is_aware(now):
            now = timezone.localtime(now)

        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        if today.month == 1:
            previous_month = today.replace(year=today.year - 1, month=1, day=1)
        else:
            previous_month = today.replace(month=today.month - 1, day=1)

        date_filter = list(self.links)
        date_filter.insert(3, ('Previous month', {
            self.lookup_kwarg_since: str(previous_month),
            self.lookup_kwarg_until: str(today.replace(day=1)),
        }))
        self.links = tuple(date_filter)


class ForeignKeyFilter(RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'
