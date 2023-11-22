import paayes
paayes.api_key = 'sk_NDAyNTAxOTc3MTU2NDY3MTksKEq00Eq01UiisKa0A0UiiNTEyOTk1OTQ1NjU0MDUyMwsKEq00Eq01UiisKEq00Eq01Uii58566'

session = paayes.checkout.Session.create(
    api_key='sk_test_4eC39HqLyjWDarjtT1zdp7dc',
    line_items=[{
      'price_data': {
        'currency': 'usd',
        'product_data': {
          'name': 'T-shirt',
        },
        'unit_amount': 2000,
      },
      'quantity': 1,
    }],
    mode='payment',
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
  )
print(session)