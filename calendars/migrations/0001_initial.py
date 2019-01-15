# Generated by Django 2.1.3 on 2019-01-14 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventTypeDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('rtl_name', models.CharField(blank=True, default='تایپ', max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'EventTypeDB',
                'verbose_name_plural': 'EventTypeDBs',
                'db_table': 'event_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(blank=True, db_index=True, null=True, unique=True)),
                ('event_note', models.CharField(help_text='Textual Notes', max_length=127)),
                ('event_date', models.DateField(help_text='Day of the event')),
                ('event_time', models.TimeField(help_text='Time of the Event')),
                ('end_time', models.TimeField(blank=True, help_text='Time of the Event', null=True)),
                ('time_to_start_notifying', models.TimeField(blank=True, help_text='Notifying time', null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'get_latest_by': ['-event_time', 'event_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventTypeChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventType_id', models.PositiveSmallIntegerField(choices=[(1, 'Medicine'), (2, 'Appointment'), (3, 'Personal'), (4, 'Holiday'), (5, 'Formal_Holiday')])),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='eventTypes',
            field=models.ManyToManyField(to='calendars.EventTypeChoice'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]