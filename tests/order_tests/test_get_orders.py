import allure

from errors import NO_AUTH_ERROR
from helpers import *
from methods.user_methods import *
from methods.order_methods import *


class TestGetOrders:

    @allure.title("api/orders: 200 ok -> успешное получение списка заказов пользователя")
    @allure.description("Проверяем успешное получение заказов и структуру ответа")
    def test_get_order(self, user_create):
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
        create_order(payload, token)
        response_get_order = get_orders(token)
        expected_order = {
            "ingredients": [id],
            "_id": response_get_order.json().get("orders")[0].get("_id"),  # Получаем _id из ответа
            "status": response_get_order.json().get("orders")[0].get("status"),
            "name": response_get_order.json().get("orders")[0].get("name"),
            "createdAt": response_get_order.json().get("orders")[0].get("createdAt"),
            "updatedAt": response_get_order.json().get("orders")[0].get("updatedAt"),
            "number": response_get_order.json().get("orders")[0].get("number"),
        }

        assert (response_get_order.status_code == 200
                and response_get_order.json().get("success") is True
                and response_get_order.json().get("orders") == [expected_order])

    @allure.title("api/orders: 200 ok -> успешное получение пустого списка заказов пользователя")
    def test_get_order_no_orders(self, user_create):
        password, email, name, access_token = user_create
        login_payload = {
            "email": email,
            "password": password,
        }
        response_login = login_user(login_payload)
        token = response_login.json().get("accessToken")
        response_get_order = get_orders(token)

        assert (response_get_order.status_code == 200
                and response_get_order.json().get("success") is True
                and response_get_order.json().get("orders") == [])

    @allure.title("api/orders: 401 unauthorized -> получение списка заказов без авторизации")
    def test_get_order_unauth(self):
        response_get_order = get_orders("")

        assert (response_get_order.status_code == 401
                and response_get_order.json().get("message") == NO_AUTH_ERROR)