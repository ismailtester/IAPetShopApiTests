import allure
import requests

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