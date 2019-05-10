"""myprj2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.static import serve

from tools import views
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index.html', views.index),
    path('contact.html', views.contact),
    path('dbs.html', views.dbs),
    path('alldt.html', views.alldt),
    path('partdt.html', views.partdt),
    path('tools/searchgexp', views.searchgexp),
    url(r'^index/static/(?P<path>.*)$', serve, {'document_root': os.path.join(BASE_DIR, "static")}),
    path('tools/searchgexp2', views.searchgexp2),
    url(r'^down_runlist', views.down_runlist),
    url(r'^down_genelist', views.down_genelist),
]
