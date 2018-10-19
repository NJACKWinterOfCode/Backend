from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/add/(?P<dbname>[-\w]+)/$',
        views.DB_detailsAPI.as_view(), name='DB_details'),
]
