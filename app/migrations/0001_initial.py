# Generated by Django 2.1 on 2018-10-21 01:13

import app.models.items
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name': 'API token',
                'verbose_name_plural': 'Access tokens',
            },
        ),
        migrations.CreateModel(
            name='Astronaut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('photo', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=90, size=[1200, 1200], upload_to=app.models.items.upload_to)),
                ('biography', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Astronaut',
                'verbose_name_plural': 'Astronauts',
            },
        ),
        migrations.CreateModel(
            name='Launch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_dt', models.DateTimeField(blank=True, null=True)),
                ('window_start_dt', models.DateTimeField(blank=True, null=True)),
                ('window_close_dt', models.DateTimeField(blank=True, null=True)),
                ('mission', models.CharField(blank=True, max_length=255, null=True)),
                ('mission_type', models.CharField(blank=True, max_length=255, null=True)),
                ('mission_description', models.TextField(blank=True, null=True)),
                ('is_crewed', models.BooleanField(default=False)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=90, size=[1200, 1200], upload_to=app.models.items.upload_to)),
                ('video', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('tbd', 'TBD'), ('ready', 'Ready'), ('in_flight', 'In Flight'), ('success', 'Success'), ('hold', 'Hold'), ('failure', 'Failure'), ('partial_failure', 'Partial Failure')], default='tbd', max_length=10, verbose_name='Status')),
                ('hold_reason', models.TextField(blank=True, null=True)),
                ('failure_reason', models.TextField(blank=True, null=True)),
                ('info_url', models.CharField(blank=True, max_length=255, null=True)),
                ('stream_url', models.CharField(blank=True, max_length=255, null=True)),
                ('hashtag', models.CharField(blank=True, max_length=255, null=True)),
                ('external_id', models.IntegerField(blank=True, null=True)),
                ('updated_dt', models.DateTimeField(blank=True, null=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('modified_dt', models.DateTimeField(auto_now=True)),
                ('astronauts', models.ManyToManyField(blank=True, to='app.Astronaut')),
            ],
            options={
                'verbose_name': 'Launch',
                'verbose_name_plural': 'Launches',
            },
        ),
        migrations.CreateModel(
            name='Rocket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('configuration', models.CharField(blank=True, max_length=255, null=True)),
                ('family', models.CharField(blank=True, max_length=255, null=True)),
                ('exploitation_start_dt', models.DateTimeField(blank=True, null=True)),
                ('exploitation_end_dt', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('wiki_url', models.CharField(blank=True, max_length=255, null=True)),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=90, size=[1920, 1920], upload_to=app.models.items.upload_to)),
                ('external_id', models.IntegerField(blank=True, null=True)),
                ('updated_dt', models.DateTimeField(blank=True, null=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('modified_dt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Rocket',
                'verbose_name_plural': 'Rockets',
            },
        ),
        migrations.CreateModel(
            name='RocketPad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.CharField(blank=True, max_length=255, null=True)),
                ('longitude', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'RocketPad',
                'verbose_name_plural': 'RocketPads',
            },
        ),
        migrations.CreateModel(
            name='SpaceAgency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('abbrev', models.CharField(blank=True, max_length=255, null=True)),
                ('country_code', models.CharField(blank=True, max_length=1000, null=True)),
                ('type', models.CharField(choices=[('government', 'Government'), ('multinational', 'Multinational'), ('commercial', 'Commercial'), ('educational', 'Educational'), ('private', 'Private'), ('unknown', 'Unknown')], default='unknown', max_length=255, verbose_name='Type')),
                ('description', models.TextField(blank=True, null=True)),
                ('website_url', models.CharField(blank=True, max_length=255, null=True)),
                ('wiki_url', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=90, size=[1200, 1200], upload_to=app.models.items.upload_to)),
                ('is_lsp', models.BooleanField(default=False)),
                ('external_id', models.IntegerField(blank=True, null=True)),
                ('updated_dt', models.DateTimeField(blank=True, null=True)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('modified_dt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'SpaceAgency',
                'verbose_name_plural': 'SpaceAgencies',
            },
        ),
        migrations.CreateModel(
            name='SpacePort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('country_code', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'SpacePort',
                'verbose_name_plural': 'SpacePorts',
            },
        ),
        migrations.AddField(
            model_name='rocketpad',
            name='space_port',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SpacePort'),
        ),
        migrations.AddField(
            model_name='rocket',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.SpaceAgency'),
        ),
        migrations.AddField(
            model_name='launch',
            name='rocket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Rocket'),
        ),
        migrations.AddField(
            model_name='launch',
            name='rocket_pad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.RocketPad'),
        ),
        migrations.AddField(
            model_name='launch',
            name='space_agency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SpaceAgency'),
        ),
        migrations.AddField(
            model_name='astronaut',
            name='space_agency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SpaceAgency'),
        ),
    ]
