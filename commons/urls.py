from django.urls import path
from .views import test, permission_controller_test
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', permission_controller_test, name = 'perm_controll'),
]