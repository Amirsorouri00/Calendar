from django.urls import include, path
from calendars.views.rest.event import test1 as event_test1, test2 as event_test2, test as event_test, \
                SingleEvent, EventListCreate

app_name = 'calendars'

urlpatterns = [
    path('form/', include(([
        
    ], 'calendars'), namespace='form')),

    path('rest/', include(([

        path('event/', include(([
            path('', SingleEvent.as_view(), name='single_event_view'),
            path('<int:uuid>/', SingleEvent.as_view(), name='single_event_view1'),
            path('list/', EventListCreate.as_view(), name='list_event_view'),
            path('test2/', event_test2, name='rest_event_test2'),
            path('test1/', event_test1, name='rest_event_test1'),
            path('test/', event_test, name='rest_event_test'),
            
        ], 'calendars'), namespace='rest_events')),
        
    ], 'calendars'), namespace='rest')),
]