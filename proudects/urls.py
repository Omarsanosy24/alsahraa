from rest_framework import routers
from . import views
from django.urls import include, path

router = routers.DefaultRouter()
router.register('products', views.ProductsView)
router.register('category', views.CategoryView)
router.register('banners', views.BannersView)
router.register('rate', views.RateView)
router.register('images', views.ImageView)
router.register('subCategory', views.SubCatView)

urlpatterns = [
    path('', include(router.urls)),
]