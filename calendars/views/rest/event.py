import datetime
from calendars.serializers.event_serializer import EventSerializer as ES
from django.http import JsonResponse
from calendars.models import Event, EventTypeChoice
from accounts.models import User

def test2(request, format=None):
    # print(request.POST)
    events = Event.objects.all()
    events_serializer = ES(events, many = True)
    print('events serialized result = {0}'.format(events_serializer))

    # print(serializer)
    # print(users_serializer.is_valid())
    # print(serializer.errors)
    # print(serializer.validated_data)
    # serializer.save()
    return JsonResponse({'received data': events_serializer.data}, safe=False, status=200)


def test1(request, format=None):
    print(request.POST)
    serializer = ES(data = request.POST)

    print(serializer)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)
    # serializer.save()

    return JsonResponse({'received data': request.POST}, safe=False, status=200)

def test(request, format=None):
    time = datetime.datetime.now().time()
    date = datetime.datetime.now().date()
    event_note = "{0}".format(time)
    user = User.objects.get(id=1)
    event = Event.objects.create(
        user=user, event_note=event_note, event_date=date, event_time=time)
    event.save()

    event_type = EventTypeChoice(eventType_id = (event.id % 5) + 1)
    event.eventTypes.add(event_type)
    
    serializer.save()

    return JsonResponse({'created event: ': event}, safe=False, status=200)
