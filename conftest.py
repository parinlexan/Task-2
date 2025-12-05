import pytest

from helpers import *
from methods.user_methods import *


@pytest.fixture
def user_create():
    email = generate_email()
    password = generate_password()
    name = generate_name()
    payload = {
        "email": email,
        "password": password,
        "name": name,
    }
    response_created = create_user(payload)
    access_token = response_created.json().get("accessToken")

    yield password, email, name, access_token

    delete_response = delete_user(access_token)
    assert delete_response.status_code == 202