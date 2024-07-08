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


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/urls')
def post_urls():
    url = request.form.get('url', '')
    #
    if validate(url):
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 402
    #
    url = urlparse(url)
    correct_url = f'{url.scheme}://{url.netloc}'
    #
    url_id = db.add_url(correct_url)
    if url_id is not None:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url', id=url_id[0]))

    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=url_id[0]))


@app.get('/urls/<int:id>')
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    url, created_at = db.get_url_info_by_id(id)
    return render_template('url.html',
                           messages=messages,
                           id=id,
                           url=url,
                           created_at=created_at)


def validate(site):
    if not validators.url(site):
        flash('Некорректный URL', 'error')
    elif len(site) > 255:
        flash('URL не должен превышать 255 символов', 'error')
    else:
        return False
    return True
