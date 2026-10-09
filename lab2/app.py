
from flask import Flask, render_template, request

app = Flask(__name__)

profile = {
    "name": "Дмитро Івасюк",
    "role": "Software Engineering Student",
    "location": "Україна",
    "email": "dmytro.ivasiuk.24@pnu.edu.ua",
    "about": "Я студент третього курсу спеціальності «Інженерія програмного забезпечення». Цікавлюся веброзробкою, програмуванням та сучасними технологіями. Постійно вдосконалюю свої навички й працюю над навчальними проєктами.",
    "education": {
        "degree": "Інженерія програмного забезпечення",
        "level": "Бакалаврат, 3 курс",
        "period": "2024 — теперішній час"
    },
    "skills": [
        "Веброзробка",
        "Об'єктно-орієнтоване програмування",
        "Робота з базами даних",
        "Git та GitHub",
        "Розробка REST API",
        "Командна робота"
    ],
    "technologies": [
        "Python", "Flask", "PHP", "HTML5",
        "CSS3", "Bootstrap", "JavaScript",
        "SQL", "Git", "GitHub"
    ],
    "projects": [
        {
            "number": "01",
            "title": "Flask Web Application",
            "description": "Навчальний вебзастосунок на Python та Flask із налаштованими маршрутами та розгортанням на Render.",
            "tags": ["Python", "Flask", "Render"]
        },
        {
            "number": "02",
            "title": "PHP Laboratory Projects",
            "description": "Серія навчальних вебпроєктів із використанням PHP, HTML, форм, обробки файлів та ООП.",
            "tags": ["PHP", "HTML", "CSS"]
        },
        {
            "number": "03",
            "title": "Personal Portfolio",
            "description": "Адаптивний сайт-портфоліо з використанням Flask, Jinja2, Bootstrap та власних стилів.",
            "tags": ["Flask", "Jinja2", "Bootstrap"]
        }
    ]
}


@app.route("/")
@app.route("/resume")
def resume():
    return render_template(
        "resume.html",
        title="Резюме | Дмитро Івасюк",
        page="resume",
        profile=profile
    )


@app.route("/contacts", methods=["GET", "POST"])
def contacts():
    success = False

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if name and email and message:
            success = True

    return render_template(
        "contacts.html",
        title="Контакти | Дмитро Івасюк",
        page="contacts",
        profile=profile,
        success=success
    )


if __name__ == "__main__":
    app.run(debug=True)
