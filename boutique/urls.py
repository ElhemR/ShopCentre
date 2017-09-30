from django.conf.urls import url
from . import views

app_name = 'boutique'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<boutique_id>[0-9]+)/$', views.detail, name='detail'),
  
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.products, name='products'),
    url(r'^create_boutique$', views.create_boutique, name='create_boutique'),
    url(r'^(?P<boutique_id>[0-9]+)/create_product/$', views.create_product, name='create_product')
 
]
