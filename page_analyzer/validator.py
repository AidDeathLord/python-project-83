import validators
from flask import flash


def validate(url):
    if not validators.url(url):
        flash('Некорректный URL', 'error')
    elif len(url) > 255:
        flash('URL не должен превышать 255 символов', 'error')
    else:
        return False
    return True
