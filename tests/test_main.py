from fastapi.testclient import TestClient
from app.main import app, Plant
import pytest

# Создаем клиент для тестирования
client = TestClient(app)


# Тест главной страницы
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Добро пожаловать в базу данных растений магазина!" in response.text


# Тест получения списка всех растений
def test_get_plants():
    response = client.get("/plants/")
    assert response.status_code == 200
    plants = response.json()
    assert isinstance(plants, list)
    assert len(plants) > 0  # Убедимся, что список не пустой


# Тест получения информации о конкретном растении
def test_get_plant():
    # Проверяем существующее растение
    response = client.get("/plants/1")
    assert response.status_code == 200
    plant = response.json()
    assert plant["id"] == 1
    assert plant["name"] == "Кактус"

    # Проверяем запрос к несуществующему растению
    response = client.get("/plants/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Растение не найдено"


# Тест добавления нового растения
def test_add_plant():
    new_plant_data = {
        "id": 4,
        "name": "Фикус",
        "species": "Ficus benjamina",
        "description": "Любит свет и умеренный полив.",
        "age_years": 2,
        "watering_frequency": "Раз в неделю",
        "price": 600.0
    }
    response = client.post("/plants/", json=new_plant_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Растение успешно добавлено"
    assert response.json()["plant"]["name"] == "Фикус"

    # Проверяем, что растение действительно добавлено
    response = client.get("/plants/4")
    assert response.status_code == 200
    assert response.json()["name"] == "Фикус"

    # Попытка добавить растение с уже существующим ID
    response = client.post("/plants/", json=new_plant_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Растение с указанным ID уже существует"


# Тест обновления информации о растении
def test_update_plant():
    updated_plant_data = {
        "id": 1,
        "name": "Обновленный Кактус",
        "species": "Cactaceae",
        "description": "Требует минимум ухода.",
        "age_years": 6,
        "watering_frequency": "Раз в месяц",
        "price": 300.0
    }
    response = client.put("/plants/1", json=updated_plant_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Информация о растении обновлена"
    assert response.json()["plant"]["name"] == "Обновленный Кактус"

    # Проверяем, что информация действительно обновлена
    response = client.get("/plants/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Обновленный Кактус"

    # Попытка обновить несуществующее растение
    response = client.put("/plants/999", json=updated_plant_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Растение не найдено"


# Тест удаления растения
def test_delete_plant():
    # Добавляем новое растение для теста удаления
    new_plant_data = {
        "id": 5,
        "name": "Тестовое растение",
        "species": "Test species",
        "description": "Тестовое описание.",
        "age_years": 1,
        "watering_frequency": "Раз в день",
        "price": 100.0
    }
    client.post("/plants/", json=new_plant_data)

    # Удаляем растение
    response = client.delete("/plants/5")
    assert response.status_code == 200
    assert response.json()["message"] == "Растение удалено"

    # Проверяем, что растение действительно удалено
    response = client.get("/plants/5")
    assert response.status_code == 404
    assert response.json()["detail"] == "Растение не найдено"

    # Попытка удалить несуществующее растение
    response = client.delete("/plants/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Растение не найдено"


# Фикстура для сброса базы данных перед каждым тестом
@pytest.fixture(autouse=True)
def reset_db():
    global plants_db
    plants_db = [
        Plant(id=1, name="Кактус", species="Cactaceae", description="Требует минимум ухода.", age_years=5,
              watering_frequency="Раз в месяц", price=250.0),
        Plant(id=2, name="Фиалка", species="Saintpaulia", description="Любит влажную почву.", age_years=3,
              watering_frequency="Раз в неделю", price=450.0),
        Plant(id=3, name="Монстера", species="Monstera deliciosa", description="Популярное декоративное растение.",
              age_years=7, watering_frequency="Два раза в неделю", price=1800.0)
    ]
    yield
