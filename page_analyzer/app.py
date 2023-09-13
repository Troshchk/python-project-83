from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')

@app.get("/")
def main_page():
    return render_template("main.html", errors = None)


@app.post("/urls")
def add_url():
    url_to_add = request.form.to_dict()["url"]
    if validators.url(url_to_add) and len(url_to_add)<256:
        try:
            conn = psycopg2.connect(DATABASE_URL)
        except:
            print('Can`t establish connection to database')
        with conn.cursor() as curs:
            curs.execute('SELECT id FROM urls WHERE name=%s', (url_to_add,))
            id = curs.fetchall()
        if len(id)>0:
            flash('Страница уже существует', 'info')
            return redirect(url_for('show_url_by_id', id=id[0][0]))
        with conn.cursor() as curs:
            curs.execute('INSERT INTO urls(name, created_at) VALUES (%s, %s)', (url_to_add, date.today().isoformat(),))
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
        curs.execute('SELECT * FROM urls ORDER BY id DESC')
        urls = curs.fetchall()
    conn.close()
    return render_template('urls_all.html', urls=urls)



@app.get("/sites")
def sites_get():
    return "Sites"
