from django.conf.urls import url

from . import views

app_name = 'summaries'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^finish/$', views.finish, name='finish'),
    url(r'^the_end/$', views.the_end, name='the_end'),
    url(r'^all_smells/$', views.all_smells, name='all_smells'),
    url(r'^design_problems/$', views.design_problems, name='design_problems'),
    url(r'^(?P<summary_id>[0-9]+)/$', views.details, name='details'),
    url(r'^(?P<summary_id>[0-9]+)/save/$', views.save, name='save'),
    url(r'^(?P<summary_id>[0-9]+)/save_smells_relevance/$', views.save_smells_relevance, name='save_smells_relevance'),
    url(r'^(?P<summary_id>[0-9]+)/smells_relevance/$', views.smells_relevance, name='smells_relevance')
]