import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers

from calendars.models import Event, EventTypeChoice
from commons import serializers as cserializers


class EventTypeField(serializers.Field):
    
    def to_representation(self, instance):
        ret = []
        for value in instance.eventTypes.all():
            print(value)
            tmp = {
                "role_id": value.eventType_id,
                "role_name": value.get_id_display()
            }
            ret.append(tmp)
        return ret

    # def to_internal_value(self, data):
    #     ret = {
    #         "role_id": data["x"],
    #         "y_coordinate": data["y"],
    #     }
    #     return ret

class EventSerializer(cserializers.DynamicFieldsModelSerializer):
    hello = serializers.SerializerMethodField('get_excluder') # define separate field
    exclud = serializers.SerializerMethodField() # define separate field
    present_time = serializers.SerializerMethodField() # define separate field
    event_types = EventTypeField(source='*')
    # popularity = serializers.IntegerField() # popularity is a defined method in the model
    
    class Meta:
        model = Event
        fields = ('id', 'uuid', 'user', 'event_note', 'event_date', 'event_time', 'end_time', 'time_to_start_notifying',
                  'created_at', 'present_time', 'event_types', 'hello', 'exclud')
        read_only_fields = ('id', 'uuid', 'created_at', 'present_time',
                            'time_to_start_notifying', 'hello', 'exclud')
        # extra_kwargs = {'username': {'write_only': True}}
        # exclude = ['user_uuid']

    def create(self, validated_data):
        #Edit
        event = Event(**validated_data)
        event.save()
        return event

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.uuid = validated_data.get('uuid', instance.uuid)
        instance.event_note = validated_data.get('event_note', instance.username)
        #Edit
        instance.save()
        return instance

    def get_present_time(self, obj):
        # return ''
        return datetime.datetime.now()

    def get_excluder(self, obj):
        # return obj.id :Example
        return 'excluder'

    def get_exclud(self, obj):
        # return ''
        return 'exclud'
    
    def _includer():
        return '_includer'


