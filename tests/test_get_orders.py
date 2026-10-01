import allure
import requests
from helpers import BASE_URL


@allure.feature("Получение заказов")
class TestGetOrders:

    @allure.title("Получение списка заказов")
    def test_get_orders(self):
        response = requests.get(
            f"{BASE_URL}/orders"
        )

        assert response.status_code == 200
        assert "orders" in response.json()
