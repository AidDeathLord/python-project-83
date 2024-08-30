from flask import (Flask,
                   render_template,
                   request,
                   get_flashed_messages,
                   flash,
                   url_for,
                   redirect)
from dotenv import load_dotenv
from urllib.parse import urlparse
import page_analyzer.postgres_requests as db
import validators
import os
import requests


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/urls')
def urls():
    _urls = db.get_all_urls()
    return render_template('urls.html', urls=_urls)


@app.post('/url')
def post_urls():
    url = request.form.get('url', '')

    # проверяем существует ли сайт, если нет - возвращаем оповещение
    if validate(url):
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 402

    # преобразуем ссылку к нужному формату
    url = urlparse(url)
    correct_url = f'{url.scheme}://{url.netloc}'

    # если ссылка уже есть получаем id
    # и переходим на страницу ссылки
    check = db.check_url(correct_url)
    if check:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url', id=check))

    # добавляем ссылку в базу, получаем ее id
    # переходим на страницу сайта по его id в базе
    url_id = db.add_url(correct_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=url_id))


@app.get('/urls/<int:id>')
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    url_info = db.get_url_info_by_id(id)
    url_checks = db.get_all_checks_for_url(id)
    return render_template('url.html',
                           messages=messages,
                           id=id,
                           url=url_info.name,
                           created_at=url_info.created_at,
                           url_checks=url_checks)


@app.post('/urls/<id>/checks')
def post_checks(id):
    url_info = db.get_url_info_by_id(id)

    try:
        response = requests.get(url_info.name)
        response.raise_for_status()
    except requests.exceptions.RequestException():
        flash('Произошла ошибка при проверке', 'error')
        return render_template('url.html',
                               id=id,
                               url=url_info.name,
                               created_at=url_info.created_at,
                               url_checks=db.get_all_checks_for_url(id))

    db.add_check(id, response.status_code)
    return redirect(url_for('get_url', id=id))


def validate(url):
    if not validators.url(url):
        flash('Некорректный URL', 'error')
    elif len(url) > 255:
        flash('URL не должен превышать 255 символов', 'error')
    else:
        return False
    return True
