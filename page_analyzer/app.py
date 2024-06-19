from dotenv import load_dotenv
from flask import Flask, render_template
import psycopg2
import os


load_dotenv()

# DATABASE_URL = os.getenv('DATABASE_URL')
# conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def hello():
    return render_template('index.html')
