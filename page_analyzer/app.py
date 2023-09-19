from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    get_flashed_messages,
)
import psycopg2
import os
from dotenv import load_dotenv
from .db_manager import DB_manager
from .url import URL
from .page_analyser import Page_analyzer

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
db_manager = DB_manager(
    connection=psycopg2.connect(DATABASE_URL), DATABASE_URL=DATABASE_URL
)
page_analyser = Page_analyzer(db_manager=db_manager)


@app.get("/")
def main_page():
    return render_template("main.html", errors=None)


@app.post("/urls")
def add_url():
    url_to_add = URL(request.form.to_dict()["url"])
    if url_to_add.is_valid():
        id_in_db = page_analyser.url_in_db(url_to_add)
        if id_in_db:
            flash("Страница уже существует", "info")
            return redirect(url_for("show_url_by_id", id=id_in_db))
        id_added = page_analyser.add_new_url_to_db(url_to_add)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("show_url_by_id", id=id_added))
    flash("Некорректный URL", "danger")
    messages = get_flashed_messages(with_categories=True)
    return render_template("main.html", messages=messages), 422


@app.get("/urls")
def show_urls():
    urls_to_show = page_analyser.format_all_urls_to_show()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "urls_all.html", urls=urls_to_show, messages=messages
    )


@app.get("/urls/<id>")
def show_url_by_id(id):
    url_to_show, checks = page_analyser.format_ind_url_to_show(id)
    if not url_to_show:
        flash("URL with this id not found", "danger")
        return redirect(url_for("show_urls"))
    messages = get_flashed_messages(with_categories=True)
    return (
        render_template(
            "individual_url.html",
            messages=messages,
            name=url_to_show.name,
            created_at=url_to_show.created_at,
            id=id,
            checks=checks,
        ),
        200,
    )


@app.post("/urls/<id>/checks")
def check_url(id):
    status_code, response = page_analyser.check_url(id)
    if status_code != 200:
        flash("Произошла ошибка при проверке", "danger")
    else:
        flash("Страница успешно проверена", "success")
        page_analyser.insert_check_to_db(id, response)
    return redirect(url_for("show_url_by_id", id=id))
