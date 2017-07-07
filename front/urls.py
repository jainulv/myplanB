from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^result/$', views.result, name='result'),
    url(r'^update/$', views.update_DB, name='update'),
]
