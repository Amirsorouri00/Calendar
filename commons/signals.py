import uuid
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import User
from calendars.models import Event
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(pre_save)
def all_models_validation(instance, *args, **kwargs):
#    instance.full_clean()
    print('all_models_are_validated')


@receiver(post_save, sender=Event)
def create_Event_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.end_time = instance.event_time
        instance.save()

@receiver(post_save, sender=User)
def create_user_UUID(sender, instance=None, created=False, **kwargs):
    if created:
        instance.uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(instance.id))
        instance.save()
