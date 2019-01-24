from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
# from commons.constants import EVENT_TYPE_COLOR_CHOICES

# Create your models here.


class EventTypeChoice(models.Model):
    '''
    The EventType entries are managed by the system,
    automatically created via a Django data migration.
    '''
    MEDICINE = 1
    APPOINTMENT = 2
    PERSONAL = 3
    HOLIDAY = 4
    FORMAL_HOLIDAY = 5
    TYPE_CHOICES = (
        (MEDICINE, 'Medicine'),
        (APPOINTMENT, 'Appointment'),
        (PERSONAL, 'Personal'),
        (HOLIDAY, 'Holiday'),
        (FORMAL_HOLIDAY, 'Formal_Holiday'),
    )
    eventType_id = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return self.get_id_display()
        # return str(self.role_id)

    def get_id_display(self):
        for key, value in self.TYPE_CHOICES:
            if self.eventType_id == key:
                return value
        return 'unknown role.'

    def get_role(self):
        for key, value in self.TYPE_CHOICES:
            if self.role_id == value:
                return {'type_id': key, 'type_name': value}
        return {'type_id': 99999, 'type_name': 'unknown role.'}


class EventTypeDB(models.Model):
    #_safedelete_policy = NO_DELETE
    name = models.CharField(max_length=63)
    rtl_name = models.CharField(
        max_length=50, default='تایپ', blank=True, null=True)
    # color = models.CharField(
    #     max_length=10, choices=EVENT_TYPE_COLOR_CHOICES, blank=True, null=True)

    class Meta:
        db_table = 'event_type'
        managed = False
        verbose_name = 'EventTypeDB'
        verbose_name_plural = 'EventTypeDBs'


class AbstractEvent(models.Model):
    #_safedelete_policy = NO_DELETE
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                             blank=True, null=True)  # change to not nullable
    event_note = models.CharField(max_length=127, help_text=u'Textual Notes',)
    event_date = models.DateField(help_text=u'Day of the event')
    event_time = models.TimeField(help_text=u'Time of the Event')
    end_time = models.TimeField(help_text=u'Time of the Event', blank=True, null=True)
    time_to_start_notifying = models.TimeField(
        help_text=u'Notifying time', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = u'Event'
        verbose_name_plural = u'Events'
        # Latest by priority descending, order_date ascending.
        get_latest_by = ['-event_time', 'event_date']

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True
        return overlap

    def get_absolute_url(self):
        url = reverse('calendar:get_one_events')
        # '''args=[self.id]'''
        return u'<a href="%s">%s</a>' % (url, str(self.event_time))

    def clean(self):
        if self.event_time <= self.end_time:
            raise ValidationError(
                'Ending hour must be after the starting hour')

        events = Event.objects.filter(event_date=self.event_date)
        if events.exists():
            for event in events:
                if self.check_overlap(event.event_time, event.end_time, self.event_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.event_time) + '-' + str(event.end_time))


class Event(AbstractEvent):
    eventTypes = models.ManyToManyField(EventTypeChoice)


class EventDB(AbstractEvent):
    eventType = models.ManyToManyField(EventTypeDB)

    class Meta:
        abstract = True
        managed = False


