from django.conf.urls import url, include

from rest_framework import routers
from apiv1 import views
from apiv1 import n11orders
from apiv1 import login

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/$', login.check),
    url(r'^n11/getorderscount/$', n11orders.getOrdersCount),
    url(r'^n11/getorders/$', n11orders.getOrders),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
