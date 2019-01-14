from django.urls import include, path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views import admins
from .views.rest.views import test2 as admin_test2, token_base_logout , CustomAuthToken
from .views.rest.user import test1 as user_test1, test2 as user_test2

app_name = 'accounts'

urlpatterns = [
    path('form/', include(([
        path('admins/', include(([
            path('', admins.AdminListView.as_view(), name='admin_list'),
            path('email_form/', admins.AdminFormView.as_view(), name='admin_list'),
            
        ], 'accounts'), namespace='admins')),

    ], 'accounts'), namespace='form')),
    

    path('rest/', include(([
        url(r'^api-token-auth/', csrf_exempt(CustomAuthToken.as_view()), name='api_token_auth'),
        path('logout/', token_base_logout, name='service_logout'),
        
        path('admins/', include(([
            path('test2/', admin_test2, name='rest_admin_test2'),
            
        ], 'accounts'), namespace='rest_admins')),

        path('user/', include(([
            path('test2/', user_test2, name='rest_user_test2'),
            path('test1/', user_test1, name='rest_user_test1'),
            
        ], 'accounts'), namespace='rest_users')),
        
    ], 'accounts'), namespace='rest')),
]