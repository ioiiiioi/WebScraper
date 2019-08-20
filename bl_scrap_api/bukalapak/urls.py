from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^api/', views.find_product, name='get_put_case'),
    # url(r'^api/(?P<pk>[0-9]+)$', views.get_put_case, name='get_put_case'),
    ]