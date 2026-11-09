# Лабораторна робота №6 — ORM SQLAlchemy та CRUD

Проєкт продовжує Flask-застосунок із лабораторної №5. Попередні модулі резюме, контактної форми, користувачів і каталогу товарів збережені. Для постів додано окрему SQLite-базу даних через Flask-SQLAlchemy.

## Запуск у Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

У ZIP уже є локальний `.env`. Для нового середовища за потреби скопіюйте `.env.example` у `.env` та задайте власний `SECRET_KEY`.

## Міграції

Папка `migrations` уже містить дві послідовні міграції, які відповідають етапам методички: початкова таблиця `posts`, потім додавання `is_active` та `author`.

```powershell
flask db history
flask db upgrade
```

Для подальших змін моделі:

```powershell
flask db migrate -m "опис змін"
flask db upgrade
```

## Запуск застосунку

```powershell
python run.py
```

Відкрийте `http://127.0.0.1:5000`.

## Маршрути постів

- `GET, POST /post/create` — створення поста.
- `GET /post` — список активних постів.
- `GET /post/<id>` — деталі поста.
- `GET, POST /post/<id>/update` — редагування.
- `GET, POST /post/<id>/delete` — підтвердження та видалення.

Автор береться із сесії `username`; якщо користувач не авторизований, записується `Anonymous`.

## Тести

```powershell
python -m unittest discover -s tests -v
```
