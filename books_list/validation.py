import validators
import datetime
from django.core.exceptions import ValidationError
from books_list.utils import normalize_date
from books_list.languages import check_name, check_code


def url_validator(url):
    if not validators.url(url):
        raise ValidationError('%(value)s is not valid url', params={'value': url})


def isbn_validator(isbn):
    if not 999999999999 < isbn < 9999999999999:
        raise ValidationError('isbn must be 13 digits long', params={'value': isbn})


def date_validator(date):
    date_new = normalize_date(date)
    date_list = date_new.split("-")

    try:
        if len(date_list) == 3:
            d = datetime.datetime.strptime(date_new, "%Y-%m-%d").date()
        elif len(date_list) == 2:
            d = datetime.datetime.strptime(date_new, "%Y-%m").date()
        elif len(date_list) == 1:
            d = datetime.datetime.strptime(date_new, "%Y").date()
        else:
            raise ValidationError('Wrong format', params={'value': date})
        if d > datetime.datetime.now().date():
            raise ValidationError('Cannot add not released books', params={'value': date})
    except ValueError:
        raise ValidationError('Wrong date', params={'value': date})


def language_validator(language):
    if not (check_code(language) or check_name(language)):
        raise ValidationError('language does not exist', params={'value': language})
