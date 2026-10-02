import allure
import pytest
from api import login_courier
from data import (
    ACCOUNT_NOT_FOUND_MESSAGE,
    LOGIN_REQUIRED_MESSAGE
)
from helpers import generate_random_string


@allure.feature("Авторизация курьера")
class TestLoginCourier:

    @allure.title("Авторизация курьера с корректными данными")
    def test_login_courier_success(self, courier):
        response = login_courier(
            courier["login"],
            courier["password"]
        )

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Авторизация курьера с неверным паролем")
    def test_login_courier_wrong_password(self, courier):
        response = login_courier(
            courier["login"],
            generate_random_string(10)
        )

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND_MESSAGE

    @allure.title("Авторизация курьера без логина")
    def test_login_courier_without_login(self, courier):
        response = login_courier(
            password=courier["password"]
        )

        assert response.status_code == 400
        assert response.json()["message"] == LOGIN_REQUIRED_MESSAGE

    @allure.title("Авторизация курьера без пароля")
    @pytest.mark.xfail(
        reason="API возвращает 504 вместо ожидаемого по документации 400"
    )
    def test_login_courier_without_password(self, courier):
        response = login_courier(
            login=courier["login"]
        )

        assert response.status_code == 400
        assert response.json()["message"] == LOGIN_REQUIRED_MESSAGE

    @allure.title("Авторизация несуществующего курьера")
    def test_login_nonexistent_courier(self):
        response = login_courier(
            generate_random_string(10),
            generate_random_string(10)
        )

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND_MESSAGE
