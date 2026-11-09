from datetime import datetime
from pathlib import Path
from tinydb import TinyDB
from flask import current_app


def get_products_table():
    db_path = Path(current_app.config["PRODUCTS_DB_PATH"])
    db_path.parent.mkdir(parents=True, exist_ok=True)

    is_new_database = not db_path.exists()

    db = TinyDB(db_path, ensure_ascii=False)
    table = db.table("products")

    if is_new_database:
        created_at = datetime.now().astimezone().isoformat(timespec="seconds")

        initial_products = [
            {
                "id": 1,
                "name": "Laptop",
                "content": "Потужний ноутбук з процесором Intel Core i7, 16 ГБ оперативної пам'яті та SSD на 512 ГБ.",
                "price": "1200.00",
                "category": "computers",
                "quantity": 5,
                "image": None,
                "created_at": created_at
            },
            {
                "id": 2,
                "name": "Phone",
                "content": "Смартфон із 6.5-дюймовим OLED-дисплеєм, подвійною камерою та акумулятором на 5000 мА·год.",
                "price": "800.00",
                "category": "phones",
                "quantity": 10,
                "image": None,
                "created_at": created_at
            },
            {
                "id": 3,
                "name": "PC",
                "content": "Настільний комп'ютер для ігор або роботи з графікою: RTX 4070, 32 ГБ RAM, 1 ТБ SSD.",
                "price": "1800.00",
                "category": "computers",
                "quantity": 3,
                "image": None,
                "created_at": created_at
            }
        ]
        for product in initial_products:
            table.insert(product)

    return table