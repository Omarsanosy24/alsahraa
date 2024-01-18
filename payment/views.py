from django.shortcuts import redirect, render
import requests
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
import traceback
from .models import order
from .models import order as Order
from dotenv import load_dotenv
import os
load_dotenv()
# Create your views here.
class OrderPermission(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method in ['GET','PATCH','PUT']:
            if request.user.is_staff:
                return True
            else:
                return False
        else:
            return True

def pay(order):
    

    url = "https://api.tap.company/v2/charges"

    payload = {
        "amount": order.total_price,
        "currency": "SAR",
        "customer_initiated": "true",
        "threeDSecure": True,
        "save_card": False,
        "description": "sample",
        "metadata": {
            "udf1": "test_data_1",
        },
        "receipt": {
            "email": True,
            "sms": True
        },
        "customer": {
            "first_name": f"{order.user.username}",
            "middle_name": f"{order.user.username}",
            "last_name": f"{order.user.username}",
            "email": f"{order.user.email}",
            "phone": {
                "country_code": "965",
                "number": f"{order.user.phone}"
            }
        },
        "source": { "id": "src_card" },
        "post": { "url": "https://api.alsahraa-abs.com/payment/data" },
        "redirect": { "url": "https://alsahraa-abs.com/en/success" }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {os.environ.get('SECRET_KEY')}"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
class OrderView(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = order.objects.filter(auth_key__isnull=False).all()
    http_method_names = ['post','get']
    permission_classes = [OrderPermission]

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        res = pay(obj)
        try:
            url = res["transaction"]['url']
            auth_id = res['id']
            obj.auth_key = auth_id
            obj.save()
        except:
            traceback.print_exc()
            return Response("some Error")
        return Response(str(url))
    
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

from rest_framework.generics import GenericAPIView

class Get_data(GenericAPIView):
    queryset = order.objects.all()
    serializer_class = FormSer

    def post(self, request):
        auth_key = request.data.get('id', None)
        if auth_key:
            res = requests.get(
                url=f'https://api.tap.company/v2/charges/{auth_key}',
                headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {os.environ.get('SECRET_KEY')}"
                }
            )
            order = Order.objects.get(auth_key=auth_key)
            order.status = res.json()['status']
            order.save(update_fields=['status'])
        return Response("done")

    def get(self, request):
        auth_key = request.query_params.get('auth_key', None)
        if auth_key:
            qs = self.queryset.filter(auth_key=auth_key)
            if qs.exists():
                qs = qs.first()
        else:
            return Response("no params")

        
        return Response((str(qs.status) if qs else "no order"))