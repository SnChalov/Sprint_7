import allure
import requests

from helpers import (
    BASE_URL,
    generate_random_string,
    login_courier,
    register_new_courier_and_return_login_password
)


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Создание курьера с корректными данными")
    def test_create_courier_success(self, cleanup_courier):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }

        response = requests.post(
            f"{BASE_URL}/courier",
            data=payload
        )

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = login_courier(
            payload["login"],
            payload["password"]
        )

        courier_id = login_response.json()["id"]
        cleanup_courier(courier_id)

    @allure.title("Создание курьера с уже существующим логином")
    def test_create_duplicate_courier(self, cleanup_courier):
        courier = register_new_courier_and_return_login_password()

        response = requests.post(
            f"{BASE_URL}/courier",
            data={
                "login": courier[0],
                "password": courier[1],
                "firstName": courier[2]
            }
        )

        assert response.status_code == 409
        assert response.json()["message"] == (
            "Этот логин уже используется. Попробуйте другой."
        )

        login_response = login_courier(
            courier[0],
            courier[1]
        )

        courier_id = login_response.json()["id"]
        cleanup_courier(courier_id)

    @allure.title("Создание курьера без логина")
    def test_create_courier_without_login(self):
        response = requests.post(
            f"{BASE_URL}/courier",
            data={
                "password": generate_random_string(10),
                "firstName": generate_random_string(10)
            }
        )

        assert response.status_code == 400
        assert response.json()["message"] == (
            "Недостаточно данных для создания учетной записи"
        )

    @allure.title("Создание курьера без пароля")
    def test_create_courier_without_password(self):
        response = requests.post(
            f"{BASE_URL}/courier",
            data={
                "login": generate_random_string(10),
                "firstName": generate_random_string(10)
            }
        )

        assert response.status_code == 400
        assert response.json()["message"] == (
            "Недостаточно данных для создания учетной записи"
        )

    @allure.title("Создание курьера без имени")
    def test_create_courier_without_first_name(self, cleanup_courier):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }

        response = requests.post(
            f"{BASE_URL}/courier",
            data=payload
        )

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = login_courier(
            payload["login"],
            payload["password"]
        )

        courier_id = login_response.json()["id"]
        cleanup_courier(courier_id)
        