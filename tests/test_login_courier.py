import allure
import requests

from helpers import (
    BASE_URL,
    generate_random_string,
    login_courier,
    register_new_courier_and_return_login_password
)


@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.title("Авторизация курьера с корректными данными")
    def test_login_courier_success(self, cleanup_courier):
        courier = register_new_courier_and_return_login_password()

        response = login_courier(
            courier[0],
            courier[1]
        )

        assert response.status_code == 200
        assert "id" in response.json()

        cleanup_courier(response.json()["id"])

    @allure.title("Авторизация курьера с неверным паролем")
    def test_login_courier_wrong_password(self, cleanup_courier):
        courier = register_new_courier_and_return_login_password()

        response = login_courier(
            courier[0],
            generate_random_string(10)
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

        login_response = login_courier(
            courier[0],
            courier[1]
        )

        cleanup_courier(login_response.json()["id"])

    @allure.title("Авторизация курьера без логина")
    def test_login_courier_without_login(self, cleanup_courier):
        courier = register_new_courier_and_return_login_password()

        response = requests.post(
            f"{BASE_URL}/courier/login",
            data={
                "password": courier[1]
            }
        )

        assert response.status_code == 400
        assert response.json()["message"] == (
            "Недостаточно данных для входа"
        )

        login_response = login_courier(
            courier[0],
            courier[1]
        )

        cleanup_courier(login_response.json()["id"])

    @allure.title("Авторизация курьера без пароля")
    def test_login_courier_without_password(self, cleanup_courier):
        courier = register_new_courier_and_return_login_password()

        response = requests.post(
            f"{BASE_URL}/courier/login",
            data={
                "login": courier[0]
            }
        )

        assert response.status_code == 504

        login_response = login_courier(
            courier[0],
            courier[1]
        )

        cleanup_courier(login_response.json()["id"])

    @allure.title("Авторизация несуществующего курьера")
    def test_login_nonexistent_courier(self):
        response = login_courier(
            generate_random_string(10),
            generate_random_string(10)
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
        