from django.shortcuts import render
from .models import *
from django.db.models import Count

# from rest_framework.viewsets import ModelViewSet
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import *
from rest_framework import filters, status
from .permission import *
from faker import Faker
from rest_framework.response import Response
import random
from django.db.models import Q

from rest_framework.decorators import action
from media import products
from main_.views import ModelViewSet

class CategoryView(ModelViewSet):
    
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializers
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
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name_ar','name_en','description_ar',"description_en",'category__name_ar',"category__name_en"]
    def get_queryset(self):
        query = self.queryset
        category_id = self.request.query_params.get('category', None)
        MainCategory_id = self.request.query_params.get('MainCategory', None)
        if category_id is not None and not " ":
            query = query.filter(Q(
                category_id=category_id
                ) | Q(
                category__subCategory=category_id
                )
                )
        if MainCategory_id is not None and not "":
            query = query.filter(Q(
                category__subCategory__mainCategory=MainCategory_id
                ) | Q(
                category__mainCategory=MainCategory_id
                ))
        return query
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
    @action(detail=False, methods=['GET'])
    def get_Varied_data(self,request):
        serializers = self.serializer_class(Product.objects.filter(star=True),many=True, context = {'request':request})
        return Response(serializers.data)
    
    @action(detail=False, permission_classes=[IsAuthenticated], methods=['GET'])
    def WishView(self,request):
        user = request.user
        wish =  user.wish.all()
        serializers = self.serializer_class(wish,many=True, context = {'request':request})
        return Response(serializers.data)
    @action(detail=False, permission_classes=[IsAuthenticated], methods=['POST'] , serializer_class= AddToWishListSer)
    def AddToWishView(self,request):
        user = request.user

        serializers = self.serializer_class(data=request.data, context = {'request':request})
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

        

class BannersView(ModelViewSet):
    queryset = Banners.objects.all()
    serializer_class = BannersSerializers
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields= ['place']
    filter_backends = [ DjangoFilterBackend]

class RateView(ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializers
    permission_classes = [IsAuthenticated]
    http_method_names=['get','post']

class ImageView(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializers
    permission_classes = [IsAdminUser]
    # http_method_names=['patch','get']

class SubCatView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminOrReadOnly]

