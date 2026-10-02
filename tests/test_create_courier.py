import allure

from api import create_courier
from data import (
    DUPLICATE_LOGIN_MESSAGE,
    MISSING_COURIER_DATA_MESSAGE
)
from helpers import generate_random_string


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Создание курьера с корректными данными")
    def test_create_courier_success(self, courier):
        assert courier["response"].status_code == 201
        assert courier["response"].json() == {"ok": True}

    @allure.title("Создание курьера с уже существующим логином")
    def test_create_duplicate_courier(self, courier):
        response = create_courier(
            login=courier["login"],
            password=courier["password"],
            first_name=courier["first_name"]
        )

        assert response.status_code == 409
        assert response.json()["message"] == DUPLICATE_LOGIN_MESSAGE

    @allure.title("Создание курьера без логина")
    def test_create_courier_without_login(self):
        response = create_courier(
            password=generate_random_string(10),
            first_name=generate_random_string(10)
        )

        assert response.status_code == 400
        assert response.json()["message"] == MISSING_COURIER_DATA_MESSAGE

    @allure.title("Создание курьера без пароля")
    def test_create_courier_without_password(self):
        response = create_courier(
            login=generate_random_string(10),
            first_name=generate_random_string(10)
        )

        assert response.status_code == 400
        assert response.json()["message"] == MISSING_COURIER_DATA_MESSAGE

    @allure.title("Создание курьера без имени")
    def test_create_courier_without_first_name(self, courier_factory):
        response, _, _ = courier_factory(
            first_name=None
        )

        assert response.status_code == 201
        assert response.json() == {"ok": True}
        