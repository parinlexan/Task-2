import random

import allure

from errors import *
from methods.order_methods import *
from methods.user_methods import *


class TestCreateOrder:

    @allure.title("api/orders: 200 ok -> успешное создание заказа с ингридиентами")
    @allure.description("Проверяем успешное создание заказа и структуру ответа")
    def test_create_order(self, user_create):
        password, email, name, access_token = user_create
        login_payload = {
            "email": email,
            "password": password,
        }
        response_login = login_user(login_payload)
        token = response_login.json().get("accessToken")
        ingrs_list = get_ingrs()
        random_ingr = random.choice(ingrs_list.json().get("data"))
        id = random_ingr.get("_id")
        payload = {
            "ingredients": [id]
        }
        response_create_order = create_order(payload, token)

        assert (response_create_order.status_code == 200
                and response_create_order.json().get("success") is True)

    @allure.title("api/orders: 400 bad request -> невозможность создания заказа без ингридиентов")
    def test_create_order_no_ingrs(self, user_create):
        password, email, name, access_token = user_create
        login_payload = {
            "email": email,
            "password": password,
        }
        response_login = login_user(login_payload)
        token = response_login.json().get("accessToken")
        payload = {
            "ingredients": []
        }
        response_create_order = create_order(payload, token)

        assert (response_create_order.status_code == 400
                and response_create_order.json().get("message") == NO_INGRS_ERROR)

    @allure.title("api/orders: 401 bad request -> невозможность создания заказа без ингридиентов")
    def test_create_order_no_auth(self):
        ingrs_list = get_ingrs()
        random_ingr = random.choice(ingrs_list.json().get("data"))
        id = random_ingr.get("_id")
        payload = {
            "ingredients": [id]
        }
        response_create_order = create_order(payload, "token")

        assert (response_create_order.status_code == 401
                and response_create_order.json().get("message") == NO_AUTH_ERROR)

    @allure.title("api/orders: 500 internal server error -> невозможность добавления в заказ ингридиента с неверным хэшем")
    def test_create_order_no_auth(self, user_create):
        password, email, name, access_token = user_create
        login_payload = {
            "email": email,
            "password": password,
        }
        response_login = login_user(login_payload)
        token = response_login.json().get("accessToken")
        payload = {
            "ingredients": ["id"]
        }
        response_create_order = create_order(payload, token)

        assert response_create_order.status_code == 500