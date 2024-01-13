from rest_framework import routers
from . import views
from django.urls import include, path

router = routers.DefaultRouter()
router.register('order', views.OrderView)


urlpatterns = [
    path('', include(router.urls)),
    path('data',views.Get_data.as_view())
]