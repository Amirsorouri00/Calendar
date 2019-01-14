from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from commons.permission_controllers import general_permission_controller as PERM_CONT
# Create your views here.

def test(request):
    return HttpResponse('In common/views/test.')

def permission_controller_test(request):
    permissions = {'healthrecords':'change_testrecord', 'healthstandards' : 'view_standardexamfieldmapping'
    , 'healthstandards' : 'add_standardexamfieldmapping'}
    
    user1 = User.objects.get(id = 1)
    print(user1)
    PERM_CONT(user1, **permissions)
    print('--------------------------------------------------------------')
    superuser = User.objects.get(username = 'amir')
    print(superuser)
    PERM_CONT(superuser, **permissions)
    return HttpResponse('in permission_controller_test: I Did It.')