from django.shortcuts import redirect, render
import requests
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
import traceback
from .models import *
# Create your views here.
api_key = "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TkRrc0ltNWhiV1VpT2lJeE5qazVNamsxT0Rrd0xqRXdORGN5TkNKOS5mcGdWbFg3UDRvSWN5UGlBZUxpNUxINGdVZDVDbmUza0lKVWhyY25NNzctd2R0OEdqNkVFTGNldElGa2F5QXA0Q2dRajdDcThMUmNnZlNqNmE3X2F1UQ=="

def payment(request):
    if request.method == 'POST':
        data = requests.post(
            "https://ksa.paymob.com/api/auth/tokens",
            json={
                "api_key":api_key
            },
        )
        token = data.json()['token']
        create_order = requests.post(
            "https://ksa.paymob.com/api/ecommerce/orders",
            json={
                "auth_token": token,
                "delivery_needed": "false",
                "amount_cents": "100",
                "currency": "SAR",
                "merchant_order_id":30,
                "items": [],
            }
        )
        
        id_= create_order.json()['id']
        payment_ = requests.post(
            "https://ksa.paymob.com/api/acceptance/payment_keys",
            json={
            "auth_token": token,
            "amount_cents": "100", 
            "expiration": 3600, 
            "order_id": id_,
            "billing_data": {
                "apartment": "803", 
                "email": "claudette09@exa.com", 
                "floor": "42", 
                "first_name": "Clifford", 
                "street": "Ethan Land", 
                "building": "8028", 
                "phone_number": "+86(8)9135210487", 
                "shipping_method": "PKG", 
                "postal_code": "01898", 
                "city": "Jaskolskiburgh", 
                "country": "CR", 
                "last_name": "Nicolas", 
                "state": "Utah"
            }, 
            "currency": "SAR", 
            "integration_id": 38
            }
        )
        token2 = payment_.json()['token']
        # return render(request , 'pay.html')
        return redirect(f"https://ksa.paymob.com/api/acceptance/iframes/24?payment_token={token2}")
    else:
        return render(request , 'pay.html')
import json
def pay(order):
    # data = requests.post(
    #     "https://api.tap.company/v2/authorize/",
    #     json={
    #         "api_key":api_key
    #     },
    # )
    # token = data.json()['token']
    # create_order = requests.post(
    #     "https://ksa.paymob.com/api/ecommerce/orders",
    #     json={
    #         "auth_token": token,
    #         "delivery_needed": "false",
    #         "amount_cents": str(order.total_price*100),
    #         "currency": "SAR",
    #         "merchant_order_id":int(order.id) + 30,
    #         "items": [],
    #     }
    # )
    
    # id_= create_order.json()['id']
    # payment_ = requests.post(
    #     "https://ksa.paymob.com/api/acceptance/payment_keys",
    #     json={
    #     "auth_token": token,
    #     "amount_cents": str(order.total_price*100), 
    #     "expiration": 3600, 
    #     "order_id": id_,
    #     "billing_data": {
    #         "apartment": "803", 
    #         "email": f"{order.user.email}", 
    #         "floor": "42", 
    #         "first_name": f"{order.user.username}", 
    #         "street": f"{order.country}", 
    #         "building": "8028", 
    #         "phone_number": f"{order.phone}", 
    #         "shipping_method": "PKG", 
    #         "postal_code": "01898", 
    #         "city": "Jaskolskiburgh", 
    #         "country": "SA", 
    #         "last_name": "Nicolas", 
    #         "state": "Utah"
    #     }, 
    #     "currency": "SAR", 
    #     "integration_id": 38
    #     }
    # )
    # token2 = payment_.json()['token']
    # return f"https://ksa.paymob.com/api/acceptance/iframes/24?payment_token={token2}"

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
        "post": { "url": "https://api.alsahraa-abs.com//payment/data" },
        "redirect": { "url": "sk_test_FHTiYzP1MonZC06JBxlQRwWA" }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer sk_test_XKokBfNWv6FIYuTMg5sLPjhJ"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
class OrderView(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = order.objects.none()
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    
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
import hmac
import hashlib
import base64

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
                    "Authorization": "Bearer sk_test_XKokBfNWv6FIYuTMg5sLPjhJ"
                }
            )
            order = order.objects.get(auth_key=auth_key)
            order.status = res['status']
        return Response("done")
