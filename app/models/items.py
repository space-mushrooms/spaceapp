import uuid

from django.db import models
from django_resized import ResizedImageField


def upload_to(instance, filename, *args, **kwargs):
    filename = filename.split('/')[-1]
    ext = ''
    if '.' in filename:
        ext = filename.split('.')[-1]
    if ext:
        filename = '{}.{}'.format(uuid.uuid4(), ext)
    return 'content/{}'.format(filename)


class SpaceAgency(models.Model):
    name = models.CharField(max_length=255)
    abbrev = models.CharField(max_length=255, null=True, blank=True)
    country_code = models.CharField(max_length=1000, null=True, blank=True)

    TYPE_GOVERNMENT = 'government'
    TYPE_MULTINATIONAL = 'multinational'
    TYPE_COMMERCIAL = 'commercial'
    TYPE_EDUCATIONAL = 'educational'
    TYPE_PRIVATE = 'private'
    TYPE_UNKNOWN = 'unknown'
    TYPE_CHOICES = (
        (TYPE_GOVERNMENT, 'Government'),
        (TYPE_MULTINATIONAL, 'Multinational'),
        (TYPE_COMMERCIAL, 'Commercial'),
        (TYPE_EDUCATIONAL, 'Educational'),
        (TYPE_PRIVATE, 'Private'),
        (TYPE_UNKNOWN, 'Unknown'),
    )
    type = models.CharField(
        max_length=255,
        default=TYPE_UNKNOWN,
        choices=TYPE_CHOICES,
        verbose_name='Type'
    )

    description = models.TextField(null=True, blank=True)
    website_url = models.CharField(max_length=255, null=True, blank=True)
    wiki_url = models.CharField(max_length=255, null=True, blank=True)
    logo = ResizedImageField(size=[1200, 1200], upload_to=upload_to, null=True, blank=True)

    is_lsp = models.BooleanField(default=False)

    external_id = models.IntegerField(null=True, blank=True)
    updated_dt = models.DateTimeField(null=True, blank=True)

    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SpaceAgency'
        verbose_name_plural = 'SpaceAgencies'

    def __str__(self):
        return '{}'.format(self.name)


class Rocket(models.Model):
    name = models.CharField(max_length=255)
    configuration = models.CharField(max_length=255, null=True, blank=True)
    family = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.ForeignKey(SpaceAgency, null=True, blank=True, on_delete=models.CASCADE)

    exploitation_start_dt = models.DateTimeField(null=True, blank=True)
    exploitation_end_dt = models.DateTimeField(null=True, blank=True)

    description = models.TextField(null=True, blank=True)

    wiki_url = models.CharField(max_length=255, null=True, blank=True)
    image = ResizedImageField(size=[1920, 1920], upload_to=upload_to, null=True, blank=True)

    external_id = models.IntegerField(null=True, blank=True)
    updated_dt = models.DateTimeField(null=True, blank=True)

    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rocket'
        verbose_name_plural = 'Rockets'

    def __str__(self):
        return '{}'.format(self.name)


class Astronaut(models.Model):
    name = models.CharField(max_length=255)

    birth_date = models.DateField(null=True, blank=True)

    space_agency = models.ForeignKey(SpaceAgency, on_delete=models.CASCADE)

    photo = ResizedImageField(size=[1200, 1200], upload_to=upload_to, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Astronaut'
        verbose_name_plural = 'Astronauts'

    def __str__(self):
        return '{}'.format(self.name)


class SpacePort(models.Model):
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'SpacePort'
        verbose_name_plural = 'SpacePorts'

    def __str__(self):
        return '{}'.format(self.name)


class RocketPad(models.Model):
    name = models.CharField(max_length=255)
    space_port = models.ForeignKey(SpacePort, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'RocketPad'
        verbose_name_plural = 'RocketPads'

    def __str__(self):
        return '{}'.format(self.name)


class Launch(models.Model):
    name = models.CharField(max_length=255)

    start_dt = models.DateTimeField(null=True, blank=True)

    window_start_dt = models.DateTimeField(null=True, blank=True)
    window_close_dt = models.DateTimeField(null=True, blank=True)

    mission = models.CharField(max_length=255, null=True, blank=True)
    mission_type = models.CharField(max_length=255, null=True, blank=True)
    mission_description = models.TextField(null=True, blank=True)

    is_crewed = models.BooleanField(default=False)
    astronauts = models.ManyToManyField(Astronaut, blank=True)

    image = ResizedImageField(size=[1200, 1200], upload_to=upload_to, null=True, blank=True)
    video = models.CharField(max_length=255, null=True, blank=True)

    rocket = models.ForeignKey(Rocket, null=True, blank=True, on_delete=models.CASCADE)
    rocket_pad = models.ForeignKey(RocketPad, null=True, blank=True, on_delete=models.CASCADE)
    space_agency = models.ForeignKey(SpaceAgency, null=True, blank=True, on_delete=models.CASCADE)

    STATUS_TBD = 'tbd'
    STATUS_READY = 'ready'
    STATUS_IN_FLIGHT = 'in_flight'
    STATUS_SUCCESS = 'success'
    STATUS_HOLD = 'hold'
    STATUS_FAILURE = 'failure'
    STATUS_PARTIAL_FAILURE = 'partial_failure'
    STATUS_CHOICES = (
        (STATUS_TBD, 'TBD'),
        (STATUS_READY, 'Ready'),
        (STATUS_IN_FLIGHT, 'In Flight'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_HOLD, 'Hold'),
        (STATUS_FAILURE, 'Failure'),
        (STATUS_PARTIAL_FAILURE, 'Partial Failure'),
    )
    status = models.CharField(
        max_length=255,
        default=STATUS_TBD,
        choices=STATUS_CHOICES,
        verbose_name='Status'
    )
    hold_reason = models.TextField(null=True, blank=True)
    failure_reason = models.TextField(null=True, blank=True)

    info_url = models.CharField(max_length=255, null=True, blank=True)
    stream_url = models.CharField(max_length=255, null=True, blank=True)
    hashtag = models.CharField(max_length=255, null=True, blank=True)

    external_id = models.IntegerField(null=True, blank=True)
    updated_dt = models.DateTimeField(null=True, blank=True)

    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Launch'
        verbose_name_plural = 'Launches'

    def __str__(self):
        return '{}'.format(self.name)
