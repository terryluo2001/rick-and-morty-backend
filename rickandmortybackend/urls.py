"""
URL configuration for rickandmortybackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from rickandmortybackend.user import (
    register,
    login,
    logout,
    details,
    update_profile,
    update_password,
)
from rickandmortybackend.favourites import (
    update_favourites,
    fetch_favourites,
    remove_favourites
)

from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('details/', details),
    path('update_profile/', update_profile),
    path('update_password/', update_password),
    path('update_favourites/', update_favourites),
    path('fetch_favourites/', fetch_favourites),
    path('remove_favourites/', remove_favourites)
]
