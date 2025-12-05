import allure

from errors import *
from helpers import generate_email, generate_name
from methods.user_methods import *


class TestEditUser:

    @allure.title("api/auth/user: 200 ok -> успешное редактирование данных пользователя")
    def test_edit_user(self, user_create):
        password, email, name, access_token = user_create
        login_payload = {
            "email": email,
            "password": password,
        }
        response_login = login_user(login_payload)
        token = response_login.json().get("accessToken")
        new_email = generate_email()
        new_name = generate_name()
        edit_payload = {
            "email": new_email,
            "name": new_name,
        }
        response_edit = edit_user(edit_payload, token)

        assert (response_edit.status_code == 200
                and response_edit.json().get("success") is True
                and response_edit.json().get("user") == {
                    "email": new_email,
                    "name": new_name,
                })

    @allure.title("api/auth/user: 401 unauthorised -> редактирование пользователя без авторизации")
    def test_edit_user_no_auth(self):
        new_email = "test@email.com"
        new_name = "nametest"
        new_payload = {
            "email": new_email,
            "name": new_name,
        }
        access_token = ""
        response_edit = edit_user(new_payload, access_token)

        assert (response_edit.status_code == 401
                and response_edit.json().get("success") is False
                and response_edit.json().get("message") == NO_AUTH_ERROR)

    @allure.title("api/auth/user: 403 forbidden -> редактирование пользователя без авторизации")
    def test_edit_user_exist_email(self, user_create):
        password, email, name, access_token = user_create
        login_payload = {
            "email": email,
            "password": password,
        }
        response_login = login_user(login_payload)
        token = response_login.json().get("accessToken")
        new_name = generate_name()
        edit_payload = {
            "email": "test@email.com",
            "name": new_name,
        }
        response_edit = edit_user(edit_payload, token)

        assert (response_edit.status_code == 403
                and response_edit.json().get("success") is False
                and response_edit.json().get("message") == EXISTING_EMAIL_ERROR)