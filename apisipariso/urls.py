from django.conf.urls import url, include

from rest_framework import routers
from apiv1 import views
from apiv1 import n11orders

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^v1/login/$', views.login),
    url(r'^v1/n11/getorderscount/$', n11orders.getOrdersCount),
    url(r'^v1/n11/getorders/$', n11orders.getOrders),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
