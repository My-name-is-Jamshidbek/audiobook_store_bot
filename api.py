import requests
import hashlib
import time

def generate_auth_header(merchant_user_id, secret_key):
    timestamp = str(int(time.time()))
    digest = hashlib.sha1((timestamp + secret_key).encode()).hexdigest()
    return f"Auth: {merchant_user_id}:{digest}:{timestamp}"

def register_with_api(merchant_id, service_id, merchant_user_id, secret_key):
    base_url = "https://api.click.uz/v2/merchant/"
    url = f"{base_url}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Auth": generate_auth_header(merchant_user_id, secret_key)
    }

    data = {
        "merchant_id": merchant_id,
        "service_id": service_id,
        "merchant_user_id": merchant_user_id
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Something went wrong"}

# Ma'lumotlarni to'ldiring
merchant_id = "34498"
service_id = "29276"
merchant_user_id = "omar"
secret_key = "mz9JPbAXItgAneaJl"

result = register_with_api(merchant_id, service_id, merchant_user_id, secret_key)
print(result)
