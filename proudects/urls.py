from rest_framework import routers
from . import views
from django.urls import include, path

router = routers.DefaultRouter()
router.register('main-category', views.MainCategoryView)
router.register('products', views.ProductsView)
router.register('category', views.CategoryView)
router.register('banners', views.BannersView)

urlpatterns = [
    path('', include(router.urls)),
]