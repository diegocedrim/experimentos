from django.conf.urls import url

from . import views

app_name = 'summaries'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^finish/$', views.finish, name='finish'),
    url(r'^the_end/$', views.the_end, name='the_end'),
    url(r'^(?P<summary_id>[0-9]+)/$', views.details, name='details'),
    url(r'^(?P<summary_id>[0-9]+)/save/$', views.save, name='save')
]