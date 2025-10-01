# api_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")

TIMEOUT = 10

def _headers(token=None):
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers



def register(username, email, password):
    payload = {"username": username, "email": email, "password": password}
    r = requests.post(f"{API_URL}/register", json=payload, timeout=TIMEOUT)
    return r

def login(username, password):
    payload = {"username": username, "password": password}
    r = requests.post(f"{API_URL}/login", json=payload, timeout=TIMEOUT)
    return r


def get_products():
    return requests.get(f"{API_URL}/products/", headers=_headers(), timeout=TIMEOUT).json()

# def get_product(product_id):
#     return requests.get(f"{API_URL}/products/{product_id}", headers=_headers(), timeout=TIMEOUT).json()


# def create_order(order_payload, token):
#     r = requests.post(f"{API_URL}/orders/", json=order_payload, headers=_headers(token), timeout=TIMEOUT)
#     return r


def add_product(payload, token):
    return requests.post(f"{API_URL}/products", json=payload, headers=_headers(token), timeout=TIMEOUT)

def update_product(payload,token):
    return requests.put(f"{API_URL}/products/{payload["id"]}", json=payload, headers=_headers(token), timeout=TIMEOUT)


def delete_product(id,token):
    return requests.delete(f"{API_URL}/products/{id}",headers = _headers(token),timeout=TIMEOUT)

def add_to_cart(payload,token):
    return requests.post(f"{API_URL}/cart/add",json=payload,headers=_headers(token),timeout=TIMEOUT)

def view_cart(token):
    return requests.get(f"{API_URL}/cart", headers=_headers(token), timeout=TIMEOUT).json()

def place_order(token):
    return requests.post(f"{API_URL}/order",headers= _headers(token),timeout=TIMEOUT)

def view_orders(token):
    # return requests.get(f"{API_URL}/order",headers=_headers(token),timeout=TIMEOUT).json()

    
    response = requests.get(f"{API_URL}/order", headers=_headers(token), timeout=TIMEOUT)
    return response.json()
    

