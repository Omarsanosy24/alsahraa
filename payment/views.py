from django.shortcuts import redirect, render
import requests
# Create your views here.
api_key = "ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TmpNMk5EZ3dMQ0p1WVcxbElqb2lNVFk0T1RNd05ESTJNQzQ0TVRVNE5USWlmUS5tblNhMXd4djBmUlNnNFREdTRuZ3dBQnc3RllYeW5jeGhwdUJDcGJpc3hFRWM4Q3YySXRnLVFKNTZwQmkxUDBYRXpzdTNsRjFKb0VqaWRocDZRZG16UQ=="

def payment(request):
    if request.method == 'POST':
        data = requests.post(
            "https://accept.paymob.com/api/auth/tokens",
            json={
                "api_key":api_key
            },
        )
        token = data.json()['token']
        create_order = requests.post(
            "https://accept.paymob.com/api/ecommerce/orders",
            json={
                "auth_token": token,
                "delivery_needed": "false",
                "amount_cents": "100",
                "currency": "EGP",
                "merchant_order_id":18,
                "items": [],
            }
        )
        id= create_order.json()['id']
        payment_ = requests.post(
            "https://accept.paymob.com/api/acceptance/payment_keys",
            json={
            "auth_token": token,
            "amount_cents": "100", 
            "expiration": 3600, 
            "order_id": id,
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
            "currency": "EGP", 
            "integration_id": 3122877
            }
        )
        token2 = payment_.json()['token']
        return redirect(f"https://accept.paymob.com/api/acceptance/iframes/703821?payment_token={token2}")
    else:
        return render(request , 'pay.html')

