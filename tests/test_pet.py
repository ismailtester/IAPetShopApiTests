import allure
import jsonschema
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
