from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^api/add_db/', views.New_DB_detailsAPI.as_view(), name='DB_details'),
    url(r'^api/get_db/', views.DBDetailsView.as_view(), name='GET_DB_details'),
    url(r'^api/get_db_details/(?P<connection_name>[-\w]+)/$', views.DBSingle.as_view(), name='GET_Single_DB_details'),
    url(r'^api/fetch_data', views.DataFetcher.as_view(), name='Fetch_Data'),
    url(r'^api/add/(?P<dbname>[-\w]+)/$',
        views.DB_detailsAPI.as_view(), name='DB_details'),
    url(r'^api/mysql/(?P<column>[-\w]+)/(?P<dbname>[-\w]+)/(?P<tablename>[-\w]+)/$',
        views.MysqlAPI.as_view(), name='Mysql'),
]
