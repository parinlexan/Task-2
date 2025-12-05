import requests

from urls import *

def create_order(payload, access_token):
    return requests.post(f'{BASE_URL}{CREATE_ORDER}', data=payload, headers={"Authorization": f"{access_token}"})

def get_orders(access_token):
    return requests.get(f'{BASE_URL}{GET_ORDERS}', headers={"Authorization": f"{access_token}"})

def get_ingrs():
    return requests.get(f'{BASE_URL}{GET_INGRS}')