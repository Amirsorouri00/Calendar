"""Calendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, , include
from accounts.views import admins as admin_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('commons/', include('commons.urls')),
    path('account/', include('accounts.urls')),
    path('calendar/', include('calendars.urls')), 
    path('accounts/signup/', admin_user.AdminSignUpView.as_view(), name='sign_up'),
    path('accounts/signup/', admin_user.AdminSignUpView.as_view(), name='home'),
]
