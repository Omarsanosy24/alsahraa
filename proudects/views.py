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
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from media import products
from main_.views import ModelViewSet
import random

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
    search_fields = ['name_ar','name_en','description_ar',"description_en",'category__name_ar',"category__name_en",'tags__name_ar','tags__name_en']
    filterset_fields =['star']
    def get_queryset(self):
        query = self.queryset
        category_id = self.request.query_params.get('category', None)
        MainCategory_id = self.request.query_params.get('MainCategory', None)
        if category_id != None and category_id != "":
            
            query = query.filter(Q(
                category_id=category_id
                ) | Q(
                category__subCategory=category_id
                )
                )
        if MainCategory_id != None and MainCategory_id != "":
            query = query.filter(Q(
                category__subCategory__mainCategory=MainCategory_id
                ) | Q(
                category__mainCategory=MainCategory_id
                ))
        
        return query
    
    @action(detail=False, methods=['GET'])
    def get_Varied_data(self,request):
        pro = Product.objects.filter().values_list('id',flat=True)        
        random_product_id_list = random.sample(list(pro),min(len(pro),20))
        query_set = Product.objects.filter(id__in=random_product_id_list)
        serializers = self.serializer_class(query_set,many=True, context={'request':request})
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
    @action(detail=False, permission_classes=[IsAuthenticated], methods=['GET'])
    def PendingOrdersView(self,request):
        user = request.user
        PendingOrders =  user.PendingOrder.all()
        serializers = self.serializer_class(PendingOrders,many=True, context = {'request':request})
        return Response(serializers.data)
    @action(detail=False, permission_classes=[IsAuthenticated], methods=['POST'] , serializer_class= PendingOrdersSer)
    def AddPendingOrdersView(self,request):
        user = request.user
        serializers = self.serializer_class(data=request.data, context = {'request':request})
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
    
    @action(detail=False, permission_classes=[IsAdminUser], methods=['POST'],serializer_class= UserIsStaff)
    def UserIsStaff(self,request):
        ser = UserIsStaff(request.data)
        if ser.is_valid():
            email = ser.data.get('email')
            try:
                user = User.objects.get(email=email)
                if user.is_staff:
                    user.is_staff = False
                else:
                    user.is_staff = True
                user.save()
            except:
                return Response(_('this email is incorrect'))
        else:
            return Response(ser.errors)
         

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
    http_method_names=['get','post','patch','delete']
    def list(self,request):
        user = request.user
        ser =self.serializer_class( self.queryset.filter(user=user), many=True, context={"request":request})
        return Response(ser.data)
    
    def update(self, request, *args, **kwargs):
        user = request.user
        if self.get_object().user == user:
            return super().update(request,*args, **kwargs)
        else:
            raise serializers.ValidationError({"permission":"you did not have permission to update it"})
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            if instance.user == request.user or request.user.is_staff:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"details":"You can not delete this commit"}, status=status.HTTP_403_FORBIDDEN)
class ImageView(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializers
    # permission_classes = [IsAdminUser]
    # http_method_names=['patch','get']

class SubCatView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    # permission_classes = [IsAdminOrReadOnly]

class LinksView(ModelViewSet):
    queryset = Links.objects.all()
    serializer_class = LinksSerializers

class MediaView(ModelViewSet):
    queryset = MediaModel.objects.all()
    serializer_class = MediaSerializers

class TagsView(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = tagsSerializersNew

class CommitView(ModelViewSet):
    queryset = commitForWeb.objects.all()
    serializer_class = CommitSerializers
    http_method_names = ['get','post','delete']
    def get_queryset(self):
        if self.request.user.is_authenticated and self.action == 'list':
            query = self.queryset.filter(user=self.request.user)
            return query
        return super().get_queryset()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_authenticated:
            if instance.user == request.user or request.user.is_staff:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"details":"You can not delete this commit"}, status=status.HTTP_403_FORBIDDEN)