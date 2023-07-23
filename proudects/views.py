from django.shortcuts import render
from .models import *
# from rest_framework.viewsets import ModelViewSet
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import *
from rest_framework import filters, status
from .permission import *
from faker import Faker
from rest_framework.response import Response
import random
from rest_framework.decorators import action
from media import products
from main_.views import ModelViewSet

class CategoryView(ModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminOrReadOnly]
    @action(detail=False, methods=['POST'])
    def create_new_data(self,request):
        fake = Faker()
        fakeAr = Faker('ar')
        for i in range(10):
            category = Category.objects.create(
                name_ar=fakeAr.name(),
                name_en=fake.name(),
            )
        return Response("done")

class ProductsView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializers
    filterset_fields= ['category','category__mainCategory']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name_ar','name_en','description_ar',"description_en",'category__name_ar',"category__name_en",'category__mainCategory__name_en']
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=False, methods=['POST'])
    def create_new_data(self,request):
        fake = Faker()
        fakeAr = Faker('ar')
        
        for i in range(10):
            pro = Product.objects.create(
                name_ar=fakeAr.name(),
                name_en=fake.name(),
                description_ar=fakeAr.name(),
                description_en=fake.name(),
                price=fake.random_int(100,1000),
                category=random.choice(Category.objects.all())
            )
            
            Image.objects.create(product=pro, image= 'products/d3b04833-ce6b-4e06-b2cd-3405c413f61a.jpeg')
            Image.objects.create(product=pro, image= 'products/face2028-eb00-4b01-be75-a4fc537a10dc.jpeg')
        return Response("done")


class BannersView(ModelViewSet):
    queryset = Banners.objects.all()
    serializer_class = BannersSerializers
    permission_classes = [IsAdminOrReadOnly]

class RateView(ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializers
    permission_classes = [IsAuthenticated]
    http_method_names=['get','post']