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
router.register('Links', views.LinksView)
router.register('media', views.MediaView)
router.register('Tags', views.TagsView)
router.register('commit', views.CommitView)

urlpatterns = [
    path('', include(router.urls)),
]