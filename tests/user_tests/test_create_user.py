import allure
import pytest


from errors import *
from helpers import *
from methods.user_methods import *


class TestCreateUser:

    @allure.title("api/auth/register -> 200 ok: все поля заполнены")
    def test_create_user(self):
        email = generate_email()
        password = generate_password()
        name = generate_name()
        payload = {
            "email": email,
            "password": password,
            "name": name,
        }
        response = create_user(payload)
        access_token = response.json().get("accessToken")

        assert (response.status_code == 200
                and response.json().get("success") is True
                and response.json().get("accessToken") == access_token
                and response.json().get("refreshToken") is not None
                and response.json().get("user") == {
                    "email": email,
                    "name": name,
                })

        delete_response = delete_user(access_token)
        assert delete_response.status_code == 202

    @allure.title("api/auth/register -> 403 forbidden: нет одного из параметров")
    @pytest.mark.parametrize("email, password, name", [
        ("", generate_password(), generate_name()),
        (generate_email(), "", generate_name()),
        (generate_email(), generate_password(), "",)
    ])
    def test_create_user_no_params(self, email, password, name):
        payload = {
            "email": email,
            "password": password,
            "name": name,
        }
        response_created = create_user(payload)

        assert (response_created.status_code == 403
                and response_created.json().get("message") == ABSENT_DATA_ERROR)

    @allure.title("api/auth/register -> 403 forbidden: создать уже созданного пользователя")
    def test_create_user_existing_user(self, user_create):
        password, email, name, access_token = user_create
        payload = {
            "email": email,
            "password": password,
            "name": name,
        }
        response_created = create_user(payload)

        assert (response_created.status_code == 403
                and response_created.json().get("message") == EXISTING_USER_ERROR)