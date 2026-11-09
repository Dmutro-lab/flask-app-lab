from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from app.forms import ContactForm

main_bp = Blueprint("main", __name__)

profile = {
    "name": "Дмитро Івасюк",
    "role": "Software Engineering Student",
    "location": "Україна",
    "email": "dmytro.ivasiuk.24@pnu.edu.ua",
    "about": "Я студент третього курсу спеціальності «Інженерія програмного забезпечення». Цікавлюся веброзробкою, програмуванням та сучасними технологіями. Постійно вдосконалюю свої навички й працюю над навчальними проєктами.",
    "education": {"degree": "Інженерія програмного забезпечення", "level": "Бакалаврат, 3 курс", "period": "2024 — теперішній час"},
    "skills": ["Веброзробка", "Об'єктно-орієнтоване програмування", "Робота з базами даних", "Git та GitHub", "Розробка REST API", "Командна робота"],
    "technologies": ["Python", "Flask", "PHP", "HTML5", "CSS3", "Bootstrap", "JavaScript", "SQL", "Git", "GitHub"],
    "projects": [
        {"number": "01", "title": "Flask Web Application", "description": "Навчальний вебзастосунок на Python та Flask із налаштованими маршрутами та розгортанням на Render.", "tags": ["Python", "Flask", "Render"]},
        {"number": "02", "title": "PHP Laboratory Projects", "description": "Серія навчальних вебпроєктів із використанням PHP, HTML, форм, обробки файлів та ООП.", "tags": ["PHP", "HTML", "CSS"]},
        {"number": "03", "title": "Personal Portfolio", "description": "Адаптивний сайт-портфоліо з використанням Flask, Jinja2, Bootstrap та власних стилів.", "tags": ["Flask", "Jinja2", "Bootstrap"]},
    ],
}


@main_bp.route("/")
@main_bp.route("/resume")
def index():
    return render_template("resume.html", title="Резюме | Дмитро Івасюк", page="resume", profile=profile)


@main_bp.route("/contacts", methods=["GET", "POST"])
@main_bp.route("/contact", methods=["GET", "POST"])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            log_path = Path(current_app.root_path).parent / "logs" / "contact.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            logger = logging.getLogger("contact_form")
            if not logger.handlers:
                handler = RotatingFileHandler(log_path, maxBytes=1024 * 1024, backupCount=3, encoding="utf-8")
                handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
            logger.info("name=%r | email=%r | subject=%r | message=%r", form.name.data, form.email.data, form.subject.data, form.message.data)
            flash("Повідомлення успішно збережено.", "success")
        except OSError:
            current_app.logger.exception("Не вдалося записати контактне повідомлення")
            flash("Не вдалося зберегти повідомлення. Спробуйте ще раз.", "danger")
        return redirect(url_for("main.contacts"))
    if request.method == "POST":
        flash("Форма містить помилки. Перевірте введені дані.", "danger")
    return render_template("contacts.html", title="Контакти | Дмитро Івасюк", page="contacts", profile=profile, form=form)


@main_bp.route("/homepage")
def home():
    return render_template("homepage.html", title="Головна | Дмитро Івасюк", page="homepage", profile=profile)
