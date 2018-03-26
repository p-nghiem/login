from django.conf.urls import url
from . import views 
urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'success$', views.success),
    url(r'create$', views.create),
    url(r'dashboard$', views.success),
    url(r'^add_to_wishlist$', views.add_to_wishlist),
    url(r'^remove_from_wishlist$', views.remove_from_wishlist),
    url(r'^delete_item$', views.delete_from_database),
    url(r'^add_new_item$', views.add_new_item)

]