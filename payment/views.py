from django.shortcuts import redirect, render
import requests
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
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

def pay(order):
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
            "amount_cents": str(order.total_price*100),
            "currency": "SAR",
            "merchant_order_id":int(order.id) + 30,
            "items": [],
        }
    )
    
    id_= create_order.json()['id']
    payment_ = requests.post(
        "https://ksa.paymob.com/api/acceptance/payment_keys",
        json={
        "auth_token": token,
        "amount_cents": str(order.total_price*100), 
        "expiration": 3600, 
        "order_id": id_,
        "billing_data": {
            "apartment": "803", 
            "email": f"{order.user.email}", 
            "floor": "42", 
            "first_name": f"{order.user.username}", 
            "street": f"{order.street}", 
            "building": "8028", 
            "phone_number": f"{order.phone}", 
            "shipping_method": "PKG", 
            "postal_code": "01898", 
            "city": "Jaskolskiburgh", 
            "country": "SA", 
            "last_name": "Nicolas", 
            "state": "Utah"
        }, 
        "currency": "SAR", 
        "integration_id": 38
        }
    )
    token2 = payment_.json()['token']
    return f"https://ksa.paymob.com/api/acceptance/iframes/24?payment_token={token2}"
class OrderView(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = order.objects.none()
    http_method_names = ['post']
    # permission_classes = [IsAuthenticated,HasAPIKey]

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        url = pay(obj)
        # print(url)
        # print(obj)
        return Response(str(url))
    
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)