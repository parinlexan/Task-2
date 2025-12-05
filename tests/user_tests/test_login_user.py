import allure

from errors import INCORRECT_LOGIN_ERROR
from methods.user_methods import login_user


class TestLoginUser:

    @allure.title("api/auth/login -> 200 ok: заходим под существующим пользователем")
    def test_login_user(self, user_create):
        password, email, name, access_token = user_create
        payload = {
            "email": email,
            "password": password,
        }
        response = login_user(payload)

        assert (response.status_code == 200
                and response.json().get("success") is True
                and response.json().get("accessToken") is not None
                and response.json().get("refreshToken") is not None
                and response.json().get("user") == {
                    "email": email,
                    "name": name,
                })

    @allure.title("api/auth/login -> 401 unauthorized: неверный пароль")
    def test_login_user_incorrect_passw(self, user_create):
        email = user_create
        payload = {
            "email": email,
            "password": "password",
        }
        response = login_user(payload)

        assert (response.status_code == 401
                and response.json().get("message") == INCORRECT_LOGIN_ERROR)

    @allure.title("api/auth/login -> 401 unauthorized: отсутствующий пароль")
    def test_login_user_no_passw(self, user_create):
        email = user_create
        payload = {
            "email": email,
            "password": "",
        }
        response = login_user(payload)

        assert (response.status_code == 401
                and response.json().get("message") == INCORRECT_LOGIN_ERROR)

    @allure.title("api/auth/login -> 401 unauthorized: некорректная почта")
    def test_login_user_incorrect_email(self, user_create):
        password = user_create
        payload = {
            "email": "email",
            "password": password,
        }
        response = login_user(payload)

        assert (response.status_code == 401
                and response.json().get("message") == INCORRECT_LOGIN_ERROR)

    @allure.title("api/auth/login -> 401 unauthorized: отсутствующая почта")
    def test_login_user_no_email(self, user_create):
        password = user_create
        payload = {
            "email": "",
            "password": password,
        }
        response = login_user(payload)

        assert (response.status_code == 401
                and response.json().get("message") == INCORRECT_LOGIN_ERROR)