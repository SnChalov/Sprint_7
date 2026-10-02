import pytest
from api import create_courier, delete_courier, login_courier
from helpers import generate_random_string


@pytest.fixture
def courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    response = create_courier(
        login=login,
        password=password,
        first_name=first_name
    )

    assert response.status_code == 201

    login_response = login_courier(login, password)

    assert login_response.status_code == 200

    courier_id = login_response.json()["id"]

    courier_data = {
        "id": courier_id,
        "login": login,
        "password": password,
        "first_name": first_name,
        "response": response
    }

    yield courier_data

    delete_courier(courier_id)


@pytest.fixture
def courier_factory():
    courier_ids = []

    def create_test_courier(
        login=None,
        password=None,
        first_name=None
    ):
        if login is None:
            login = generate_random_string(10)

        if password is None:
            password = generate_random_string(10)

        response = create_courier(
            login=login,
            password=password,
            first_name=first_name
        )

        if response.status_code == 201:
            login_response = login_courier(login, password)

            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                courier_ids.append(courier_id)

        return response, login, password

    yield create_test_courier

    for courier_id in courier_ids:
        delete_courier(courier_id)
