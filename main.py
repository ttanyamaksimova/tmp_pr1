from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

app = FastAPI()


class Plant(BaseModel):
    id: int
    name: str
    species: str
    description: str
    age_years: int
    watering_frequency: str
    price: float


# Начальные данные о растениях
plants_db = [
    Plant(id=1, name="Кактус", species="Cactaceae", description="Требует минимум ухода.", age_years=5,
          watering_frequency="Раз в месяц", price=250.0),
    Plant(id=2, name="Фиалка", species="Saintpaulia", description="Любит влажную почву.", age_years=3,
          watering_frequency="Раз в неделю", price=450.0),
    Plant(id=3, name="Монстера", species="Monstera deliciosa", description="Популярное декоративное растение.",
          age_years=7, watering_frequency="Два раза в неделю", price=1800.0)
]


# Главная страница
@app.get("/", response_class=PlainTextResponse)
def root():
    return (
        "Добро пожаловать в базу данных растений магазина!\n\n"
        "Это серверное приложение позволяет вам управлять информацией о растениях.\n\n"
        "Доступные действия:\n"
        "- GET /plants/: Получить список всех растений\n"
        "- GET /plants/{plant_id}: Получить информацию о конкретном растении по его ID\n"
        "- POST /plants/: Добавить новое растение\n"
        "- PUT /plants/{plant_id}: Обновить информацию о существующем растении\n"
        "- DELETE /plants/{plant_id}: Удалить растение"
    )


# Получение списка всех растений
@app.get("/plants/", response_model=list[Plant])
def get_plants():
    return plants_db


# Получение информации о конкретном растении по ID
@app.get("/plants/{plant_id}", response_model=Plant)
def get_plant(plant_id: int):
    for plant in plants_db:
        if plant.id == plant_id:
            return plant
    raise HTTPException(status_code=404, detail="Растение не найдено")


# Добавление нового растения
@app.post("/plants/")
def add_plant(new_plant: Plant):
    for plant in plants_db:
        if plant.id == new_plant.id:
            raise HTTPException(status_code=400, detail="Растение с указанным ID уже существует")
    plants_db.append(new_plant)
    return {"message": "Растение успешно добавлено", "plant": new_plant}


# Обновление информации о растении
@app.put("/plants/{plant_id}")
def update_plant(plant_id: int, updated_plant: Plant):
    for i, plant in enumerate(plants_db):
        if plant.id == plant_id:
            if updated_plant.id != plant_id:
                for other_plant in plants_db:
                    if other_plant.id == updated_plant.id:
                        raise HTTPException(status_code=400, detail="Новый ID уже используется другим растением")
            plants_db[i] = updated_plant
            return {"message": "Информация о растении обновлена", "plant": updated_plant}
    raise HTTPException(status_code=404, detail="Растение не найдено")


# Удаление растения
@app.delete("/plants/{plant_id}")
def delete_plant(plant_id: int):
    for i, plant in enumerate(plants_db):
        if plant.id == plant_id:
            del plants_db[i]
            return {"message": "Растение удалено"}
    raise HTTPException(status_code=404, detail="Растение не найдено")


# Запуск приложения
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
