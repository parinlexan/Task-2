import requests

from urls import *

def create_user(payload):
    return requests.post(f'{BASE_URL}{CREATE_USER}', data=payload)

def login_user(payload):
    return requests.post(f'{BASE_URL}{LOGIN_USER}', data=payload)

def edit_user(payload, access_token):
    return requests.patch(f'{BASE_URL}{EDIT_GET_DELETE_USER}', data=payload, headers={"Authorization": f"{access_token}"})

def delete_user(access_token):
    return requests.delete(f'{BASE_URL}{EDIT_GET_DELETE_USER}', headers={"Authorization": f"{access_token}"})