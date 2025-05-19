"""
URL configuration for hackmap project.

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
from django.urls import path, re_path, include
import labmap.views
import labprinter.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("map", labmap.views.map),
    path("lights", labmap.views.lights),
    path("printers", labprinter.views.Printers.as_view()),
    re_path(r"lights/(?P<ids>[0-9,]+)/(?P<val>[0-9.]+)", labmap.views.set_lights),
    re_path(r"lights/preset/(?P<preset>[A-z]+)", labmap.views.set_light_preset),
    path("", include("labdash.urls")),
]
