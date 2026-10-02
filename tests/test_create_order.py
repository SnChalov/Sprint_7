import allure
import pytest
from api import create_order


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            None
        ]
    )
    def test_create_order(self, color):
        payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Москва, ул. Тестовая, д. 1",
            "metroStation": "Сокольники",
            "phone": "+79991234567",
            "rentTime": 1,
            "deliveryDate": "2026-10-02",
            "comment": "Тестовый заказ"
        }

        if color is not None:
            payload["color"] = color

        response = create_order(payload)

        assert response.status_code == 201
        assert "track" in response.json()
