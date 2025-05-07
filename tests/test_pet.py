import allure
import jsonschema
import pytest
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца (DELETE /pet/{petId})")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", f"Текст ошибки не совпал с ожидаемым."

    @allure.title("Попытка обновить несуществующего питомца (PUT /pet)")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            body = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=body)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with (allure.step("Проверка текстового содержимого ответа")):
            assert response.text == "Pet not found", f"Текст ошибки не совпал с ожидаемым."

    @allure.title("Попытка получить информацию о несуществующем питомце (GET /pet/{petId})")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", f"Текст ошибки не совпал с ожидаемым."

    @allure.title("Добавление нового питомца (POST /pet)")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания нового питомца"):
            body = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса c информацией о питомце"):
            response = requests.post(url=f"{BASE_URL}/pet", json=body)
            response_json = response.json()

        with allure.step("Проверка кода ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответ"):
            assert body["id"] == response_json["id"], f"Ошибка в значении поля 'id'"
            assert body["name"] == response_json["name"], f"Ошибка в значении поля 'name'"
            assert body["status"] == response_json["status"], f"Ошибка в значении поля 'status'"

    @allure.title("Добавление нового питомца c полными данными (POST /pet)")
    def test_add_full_pet(self):
        with allure.step("Подготовка  данных всех полей для создания нового питомца"):
            body = {
                "id": 10,
                "name": "doggie",
                "photoUrls": ["string"],
                "tags": [{"id": 0,"name": "string"}],
                "status": "available"
            }

        with allure.step("Отправка запроса c информацией о питомце"):
            response = requests.post(url=f"{BASE_URL}/pet", json=body)
            response_json = response.json()

        with allure.step("Проверка кода ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert body["id"] == response_json["id"], f"Ошибка в значении поля 'id'"
            assert body["name"] == response_json["name"], f"Ошибка в значении поля 'name'"
            assert body["photoUrls"] == response_json["photoUrls"], f"Ошибка в значении поля 'photoUrls'"
            assert body["tags"] == response_json["tags"], f"Ошибка в значении поля 'tags'"
            assert body["status"] == response_json["status"], f"Ошибка в значении поля 'status'"

    @allure.title("Получение информации о питомце по ID (GET /pet/{petId})")
    def test_get_pet_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID "):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статус кода ответа и  параметров питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id, f"Ошибка в значении поля 'id'"
            assert response.json()["name"] == create_pet["name"], f"Ошибка в значении поля 'name'"
            assert response.json()["photoUrls"] == create_pet["photoUrls"], f"Ошибка в значении поля 'photoUrls'"
            assert response.json()["tags"] == create_pet["tags"], f"Ошибка в значении поля 'tags'"
            assert response.json()["status"] == create_pet["status"], f"Ошибка в значении поля 'status'"

    @allure.title("Обновление информации о питомце (PUT /pet)")
    def test_update_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка  данных для обновления питомца"):
            body = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }


        with allure.step("Отправка запроса на получение информации о питомце по ID "):
            response = requests.put(url=f"{BASE_URL}/pet", json=body)
            response_json = response.json()

        with allure.step("Проверка статус кода ответа и  параметров питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert body["id"] == response_json["id"], f"Ошибка в значении поля 'id'"
            assert body["name"] == response_json["name"], f"Ошибка в значении поля 'name'"
            assert body["status"] == response_json["status"], f"Ошибка в значении поля 'status'"

    @allure.title("Удаление питомца по ID (DELETE /pet/{petId})")
    def test_delete_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца по id"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статус кода ответа и сообщения об удалении"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.text == "Pet deleted", f"Неправильный текст в сообщение об удалении питомца"

        with allure.step("Отправка запроса на получение информации об удаленном питомце по ID "):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статус кода ответа на получение информации об удаленном питомце"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение списка питомцев по статусу (GET /pet/findByStatus)")
    @pytest.mark.parametrize(
        "status, expected_status_code, expected_type",
        [
            ("available", 200, list),
            ("pending", 200, list),
            ("sold", 200, list),
            ("dead", 400, dict),
            ("", 400, dict)

        ]
    )
    def test_get_pet_by_status(self, status, expected_status_code, expected_type):

        with allure.step(f"Получение списка питомцев по статусу {status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статус кода ответа и формата данных"):
            assert response.status_code == expected_status_code, "Код ответа не совпал с ожидаемым"
            print(type(response.json()))
            assert isinstance(response.json(), expected_type), f"В ответе пришел неверный формат данных" #  isinstance(response.json(), list) Проверяет соответствует ли переменная 1, формату данных
