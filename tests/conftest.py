import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

@pytest.fixture(scope="function")
def create_pet():
    """Фикстура для создания питомца"""
    body = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(url=f"{BASE_URL}/pet", json=body)
    response_json = response.json()
    assert response.status_code == 200, f"Неверный статус код"
    return response_json

@pytest.fixture(scope="function")
def create_order():
    """Фикстура для создания заказа"""
    body = {
        "id": 1,
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": True
    }
    response = requests.post(url=f"{BASE_URL}/store/order", json=body)
    response_json = response.json()
    assert response.status_code == 200, f"Неверный статус код"
    return response_json