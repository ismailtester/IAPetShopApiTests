import allure
import jsonschema
import pytest
import requests
from .schemas.order_schema import ORDER_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestStore:
    @allure.title("Размещение заказа (POST /store/order)")
    def test_placing_order(self):
        with allure.step("Подготовка данных для создания нового заказа"):
            body = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса c информацией о новом заказе"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=body)
            response_json = response.json()

        with allure.step("Проверка кода ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert body["id"] == response_json["id"], f"Ошибка в значении поля 'id'"
            assert body["petId"] == response_json["petId"], f"Ошибка в значении поля 'petId'"
            assert body["quantity"] == response_json["quantity"], f"Ошибка в значении поля 'quantity'"
            assert body["status"] == response_json["status"], f"Ошибка в значении поля 'status'"
            assert body["complete"] == response_json["complete"], f"Ошибка в значении поля 'complete'"

    @allure.title("Получение информации о заказе по ID (GET /store/order/{orderId})")
    def test_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID "):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статус кода ответа и  параметров питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == order_id, f"Ошибка в значении поля 'id'"
            assert response.json()["id"] == create_order["id"], f"Ошибка в значении поля 'id'"
            assert response.json()["petId"] == create_order["petId"], f"Ошибка в значении поля 'petId'"
            assert response.json()["quantity"] == create_order["quantity"], f"Ошибка в значении поля 'quantity'"
            assert response.json()["status"] == create_order["status"], f"Ошибка в значении поля 'status'"
            assert response.json()["complete"] == create_order["complete"], f"Ошибка в значении поля 'complete'"

    @allure.title("Удаление заказа по ID (DELETE /store/order/{orderId})")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа по id"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статус кода ответа запроса на удаление заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации об удаленном заказе по ID "):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статус кода ответа на получение информации об удаленном заказе"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществующем заказе (GET /store/order/{orderId})")
    def test_get_nonexistent_order(self, create_order):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", f"Текст ошибки не совпал с ожидаемым."

    # @allure.title("Получение инвентаря магазина (GET /store/inventory)")

