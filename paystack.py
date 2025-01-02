import requests
from config import PAYSTACK_SECRET_KEY

def initialize_payment(email, phone, amount, query_id, chat_id):
    amount_in_pesewas = amount * 100  # Convert to pesewas
    ref = f"txn-{chat_id}-{query_id}"
    
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "amount": amount_in_pesewas,
        "currency": "GHS",
        "reference": ref,
        "callback_url": "https://t.me/elitekumasidating",  # Replace with your webhook
        "metadata": {"custom_fields": [{"display_name": "Phone Number", "variable_name": "phone", "value": phone}]}
    }
    
    response = requests.post("https://api.paystack.co/transaction/initialize", json=payload, headers=headers)

    if response.status_code == 200:
        payment_data = response.json()
        return payment_data["data"]["authorization_url"]
    else:
        return None
