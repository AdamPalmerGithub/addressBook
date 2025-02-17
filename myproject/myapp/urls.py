"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.landing, name="landing"),
    path("login/", views.login, name="login"),
    path("signup/",views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("addressBook/", views.addressBook, name="addressBook"),
    path('addContact/', views.addContact, name='addContact'),
    path('settings/', views.settings,name="settings"),
    path('delete/', views.delete, name="delete"),
    path('deleteContact/<str:id>/', views.deleteContact, name='deleteContact'),
    path('updateContact/<str:id>/', views.updateContact, name='updateContact'),
    path('calendar/<str:id>', views.calendar, name='calendar'),
]
