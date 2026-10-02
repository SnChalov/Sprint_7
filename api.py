import allure
import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"


@allure.step("Создать курьера")
def create_courier(login=None, password=None, first_name=None):
    payload = {}

    if login is not None:
        payload["login"] = login

    if password is not None:
        payload["password"] = password

    if first_name is not None:
        payload["firstName"] = first_name

    return requests.post(
        f"{BASE_URL}/courier",
        data=payload
    )


@allure.step("Авторизовать курьера")
def login_courier(login=None, password=None):
    payload = {}

    if login is not None:
        payload["login"] = login

    if password is not None:
        payload["password"] = password

    return requests.post(
        f"{BASE_URL}/courier/login",
        data=payload
    )


@allure.step("Удалить курьера")
def delete_courier(courier_id):
    return requests.delete(
        f"{BASE_URL}/courier/{courier_id}"
    )


@allure.step("Создать заказ")
def create_order(payload):
    return requests.post(
        f"{BASE_URL}/orders",
        json=payload
    )


@allure.step("Получить список заказов")
def get_orders():
    return requests.get(
        f"{BASE_URL}/orders"
    )
    