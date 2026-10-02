import allure
from api import get_orders


@allure.feature("Получение заказов")
class TestGetOrders:

    @allure.title("Получение списка заказов")
    def test_get_orders(self):
        response = get_orders()

        assert response.status_code == 200
        assert "orders" in response.json()
