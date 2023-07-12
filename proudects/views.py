from django.shortcuts import render
from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import *
from rest_framework import filters, status
from .permission import *
from faker import Faker
from rest_framework.response import Response
import random
from rest_framework.decorators import action



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
    filterset_fields= ['category']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name_ar','name_en','des_ar',"des_en"]
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
        return Response("done")


class BannersView(ModelViewSet):
    queryset = Banners.objects.all()
    serializer_class = BannersSerializers
    permission_classes = [IsAdminOrReadOnly]