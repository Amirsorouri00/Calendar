from accounts.serializers.user_serializer import UserSerializer as US
from django.http import JsonResponse
from accounts.models import User

def test2(request, format=None):
    # print(request.POST)
    users = User.objects.all()
    users_serializer = US(users, many = True)
    print('user serialized result = {0}'.format(users_serializer))
    # serializer = US(data = request.POST)
    # print(serializer)
    # print(users_serializer.is_valid())
    # print(serializer.errors)
    # print(serializer.validated_data)
    # serializer.save()
    return JsonResponse({'received data': users_serializer.data}, safe=False, status=200)

def test1(request, format=None):
    print(request.POST)
    serializer = US(data = request.POST)
    print(serializer)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)
    serializer.save()
    return JsonResponse({'received data': request.POST}, safe=False, status=200)


# from django.views import View
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

@method_decorator([require_http_methods(["GET", "POST", "PUT", "DELETE"])], name='dispatch')
class SingleUser(APIView):
    serializer_class = US
    model = User

    def get(self, request, *args, **kwargs):
        user_serialized = self.serializer_class(get_object_or_404(self.model, uuid = request.GET.get('uuid')))
        return JsonResponse({'response': user_serialized.data}, safe=False, status=200)

    def post(self, request, uuid = None, *args, **kwargs):
        serializer = None
        if uuid:
            user = get_object_or_404(self.model, uuid = uuid)
            serializer = self.serializer_class(user, data = request.POST, partial=True)
        else:
            serializer = self.serializer_class(data = request.POST)
        if serializer.is_valid():
            # <process serializer cleaned data>
            # return HttpResponseRedirect('/success/')
            return JsonResponse({'received data': serializer.data}, safe=False, status=200)
        else:
            return JsonResponse({'received data': request.POST, 'errors': serializer.errors}, safe=False, status=500)

    def put(self, request, uuid, *args, **kwargs):
        user = get_object_or_404(self.model, uuid = uuid)
        serializer = self.serializer_class(user, data = request.POST, partial=True)
        if serializer.is_valid():
            # <process serializer cleaned data>
            # return HttpResponseRedirect('/success/')
            return JsonResponse({'received data': serializer.data}, safe=False, status=200)
        else:
            return JsonResponse({'received data': serializer.errors}, safe=False, status=500)

    def delete(self, request, uuid, *args, **kwargs):
        # delete an object and send a confirmation response
        from django.db.models import ProtectedError
        try:
            get_object_or_404(self.model, uuid=uuid).delete()            
            return JsonResponse({'deleted data': uuid}, safe=False, status=200)
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return JsonResponse(error_message, status=500)
        except Exception as e:
            error_message = {'errors': [str(val)] for val in e}
            return JsonResponse(error_message, safe=False, status=500)


from rest_framework import generics
# from rest_framework.permissions import IsAdminUser, IsAuthenticated

class UserListCreate(generics.ListCreateAPIView):
    ''' Used for read-write endpoints to represent a collection of model instances.
    Provides get and post method handlers. '''

    queryset = User.objects.all()
    serializer_class = US
    # permission_classes = (IsAdminUser, IsAuthenticated)

    def get_queryset(self):
        # user = User.objects.filter(id = 3)
        # print(self.request.data.get('all'))
        filter_role = {}
        # queryset = self.get_queryset()
        if self.request.data.get('all'):
            return User.objects.all()
        elif self.request.data.get('fields'):
            #change
            data = self.request.data.get('fields').strip('[').rstrip(']')
            filter_role['id'] = [{int(val) for val in data.split(',')}]
            print(filter_role)
            # return User.objects.filter(id in filter_role)
            return get_object_or_404(User.objects.all(), *filter_role)

        else: return JsonResponse({'error': 'no user specified to show.'})

    def perform_create(self, serializer):
        serializer.save(data=self.request.data)

    def perform_update(self, serializer):
        serializer.save(data=self.request.data)

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     filter = {}
    #     for field in self.multiple_lookup_fields:
    #         filter[field] = self.kwargs[field]

    #     obj = get_object_or_404(queryset, **filter)
    #     self.check_object_permissions(self.request, obj)
    #     return obj