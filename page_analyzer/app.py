from flask import Flask, render_template, request, flash, redirect, \
    url_for, get_flashed_messages
import validators
from datetime import date
import psycopg2
from psycopg2.extras import NamedTupleCursor
import os
from dotenv import load_dotenv
from collections import namedtuple

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.get("/")
def main_page():
    return render_template("main.html", errors=None)


@app.post("/urls")
def add_url():
    url_to_add = request.form.to_dict()["url"]
    if validators.url(url_to_add) and len(url_to_add) < 256:
        try:
            conn = psycopg2.connect(DATABASE_URL)
        except:
            print('Can`t establish connection to database')
        with conn.cursor() as curs:
            curs.execute('SELECT id FROM urls WHERE name=%s', (url_to_add,))
            id = curs.fetchall()
        if len(id) > 0:
            flash('Страница уже существует', 'info')
            return redirect(url_for('show_url_by_id', id=id[0][0]))
        with conn.cursor() as curs:
            curs.execute('INSERT INTO urls(name, created_at) \
                         VALUES (%s, %s)',
                         (url_to_add, date.today().isoformat(),))
            curs.execute('SELECT * FROM urls WHERE name=%s', (url_to_add,))
            conn.commit()
            curs.execute('SELECT * FROM urls WHERE name=%s', (url_to_add,))
            id = curs.fetchall()
        conn.close()
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url_by_id', id=id[0][0]))
    flash('Некорректный URL', 'danger')
    messages = get_flashed_messages(with_categories=True)
    return render_template('main.html', messages=messages), 422


@app.get("/urls")
def show_urls():
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except:
        print('Can`t establish connection to database')
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT id,name,created_at FROM urls ORDER BY id DESC')
        urls = curs.fetchall()
    url_to_show = namedtuple('URL',['id','name', 'created_at', 'last_check_created_at', "last_check_status_code"])
    urls_to_show = []
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        for url in urls:
            curs.execute('SELECT created_at,status_code FROM url_checks WHERE url_id=%s ORDER BY id DESC', (url.id,))
            check = curs.fetchone()
            print(check)
            if check:
                check_created_at = check.created_at if check.created_at else ""
                check_status_code = check.status_code if check.status_code else ""
                urls_to_show.append(url_to_show(url.id, url.name, url.created_at, check_created_at, check_status_code))
            else:
                urls_to_show.append(url_to_show(url.id, url.name, url.created_at, "", ""))
    conn.close()
    return render_template('urls_all.html', urls=urls_to_show)


@app.get("/urls/<id>")
def show_url_by_id(id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except:
        print('Can`t establish connection to database')
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls WHERE id=%s', (id,))
        url_to_show = curs.fetchall()
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM url_checks WHERE url_id=%s', (id,))
        checks = curs.fetchall()
    conn.close()
    if len(url_to_show) < 1:
        return "NOT FOUND"
    name = url_to_show[0][1]
    created_at = url_to_show[0][2]
    messages = get_flashed_messages(with_categories=True)
    return render_template('individual_url.html', messages=messages,
                           name=name, created_at=created_at, id=id, checks=checks), 200


@app.post("/urls/<id>/checks")
def check_url(id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except:
        print('Can`t establish connection to database')
    with conn.cursor() as curs:
        curs.execute('INSERT INTO url_checks(url_id, created_at) \
                     VALUES (%s, %s)',
                     (id, date.today().isoformat(),))
        conn.commit()
    conn.close()
    return redirect(url_for('show_url_by_id', id=id))
