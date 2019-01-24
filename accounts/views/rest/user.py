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
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class SingleUserView(APIView):
    serializer_class = US
    model = User

    def get(self, request, *args, **kwargs):
        user_serialized = self.serializer_class(get_object_or_404(self.model, uuid = request.GET.get('uuid')))
        return JsonResponse({'response': user_serialized.data}, safe=False, status=200)

    def post(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(data = request.POST)
        if serializer.is_valid():
            # <process serializer cleaned data>
            # return HttpResponseRedirect('/success/')
            return JsonResponse({'received data': serializer.data}, safe=False, status=200)
        else:
            return JsonResponse({'received data': request.POST, 'errors': serializer.errors}, safe=False, status=500)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(self.model, uuid = request.PUT.get('uuid'))
        serializer = self.serializer_class(user, data = request.PUT, partial=True)
        if serializer.is_valid():
            # <process serializer cleaned data>
            # return HttpResponseRedirect('/success/')
            return JsonResponse({'received data': serializer.data}, safe=False, status=200)
        else:
            return JsonResponse({'received data': serializer.errors}, safe=False, status=500)

    def delete(self, request, *args, **kwargs):
        # delete an object and send a confirmation response
        from django.db.models import ProtectedError
        try:
            get_object_or_404(self.model, uuid=request.DELETE('uuid')).delete()            
            return JsonResponse({'deleted data': request.DELETE('uuid')}, safe=False, status=200)
        except ProtectedError:
            error_message = "This object can't be deleted!!"
            return JsonResponse(error_message, status=500)
        except Exception as e:
            error_message = "request.Delete doesnt exist. "
            return JsonResponse(error_message, safe=False, status=500)

