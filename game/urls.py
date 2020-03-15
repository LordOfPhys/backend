"""game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from app import views
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'index/', views.index, name = 'index'),
    url(r'^login/$', views.log, name = 'login'),
    url(r'^take_numbers/$', views.take_numbers, name = 'take_numbers'),
    url(r'^startgame/$', views.start_game, name = 'startgame'),
    url(r'^toKillUser/$', views.toKillUser, name = 'toKillUser'),
    url(r'^logout/$', views.logout_view, name = 'logout'),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^registration/$', views.register, name = 'register'),
    url(r'^setLocation/$', views.setLocation, name = 'setLocation'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
