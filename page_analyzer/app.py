from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route("/")
def welcome():
    return render_template("main.html")


@app.get("/sites")
def sites_get():
    return "Sites"
