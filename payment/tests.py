import hmac
import hashlib


ss = bytes("sk_test_XKokBfNWv6FIYuTMg5sLPjhJ", "utf-8")
ss25 = bytes("00552d2d6371bfb89dfccec3af87e31b006292e79266eecf55bbb44187cafbb8", "utf-8")
print(ss25)


request = {
    "id": "auth_TS04A0620240348Oh9e1101078",
    "object": "authorize",
    "customer_initiated": True,
    "authorize_debit": False,
    "live_mode": False,
    "api_version": "V2",
    "status": "DECLINED",
    "amount": 1.0,
    "currency": "SAR",
    "threeDSecure": True,
    "save_card": False,
    "merchant_id": "",
    "product": "",
    "statement_descriptor": "sample",
    "transaction": {
        "timezone": "UTC+03:00",
        "created": "1704944911345",
        "expiry": {"period": 30, "type": "MINUTE"},
        "asynchronous": False,
        "amount": 1.0,
        "currency": "SAR",
    },
    "reference": {
        "track": "tck_TS06A0620240348Jn5x1101109",
        "payment": "6711240348011096264",
        "gateway": "00",
        "transaction": "txn_0001",
        "order": "ord_0001",
    },
    "response": {"code": "504", "message": "Declined, 3D Security - Card not Enrolled"},
    "gateway": {"response": {"code": "?"}},
    "card": {
        "object": "card",
        "first_six": "401200",
        "first_eight": "40120000",
        "scheme": "VISA",
        "brand": "VISA",
        "last_four": "0026",
    },
    "receipt": {"id": "206011240348014934", "email": True, "sms": True},
    "customer": {
        "first_name": "Test",
        "last_name": "Test",
        "email": "test@test.com",
        "phone": {"country_code": "965", "number": "50000000"},
    },
    "source": {
        "object": "token",
        "type": "CARD_NOT_PRESENT",
        "payment_type": "CREDIT",
        "payment_method": "VISA",
        "channel": "INTERNET",
        "id": "tok_Dyxl2924048tZNj11Xk0p440",
        "on_file": False,
    },
    "redirect": {"status": "PENDING", "url": "https://www.google.com/"},
    "post": {
        "status": "PENDING",
        "url": "https://3f17-156-207-60-79.ngrok-free.app/payment/data",
    },
    "auto": {"status": "CANCELLED", "type": "VOID", "time": 100},
    "merchant": {"country": "KW", "id": "599424"},
    "metadata": {"udf1": "test_data_1", "udf2": "test_data_2", "udf3": "test_data_3"},
    "order": {"id": "ord_sTBo1124048H6Ky11xC0s578"},
}
id = request['id']
amount = request['amount']
currency = request['currency']
gateway_reference = request['reference']['gateway']
payment_reference = request['reference']['payment']
status = request['status']
created = request['transaction']['created']
toBeHashedString = bytes(f'x_id{id}x_amount{amount}x_currency{currency}x_gateway_reference{gateway_reference}x_payment_reference{payment_reference}x_status{status}x_created{created} ', 'utf-8')
omar = hmac.new(msg=ss, key=toBeHashedString, digestmod=hashlib.sha256).hexdigest()
print(omar)