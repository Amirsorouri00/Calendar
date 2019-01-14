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
    # serializer.save()

    return JsonResponse({'received data': request.POST}, safe=False, status=200)