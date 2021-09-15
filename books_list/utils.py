import requests
from books_list.models import Book
from books_list.languages import check_name


def get_books_from_api(keywords):
    url = "https://www.googleapis.com/books/v1/volumes?q=" + keywords
    r = requests.get(url).json()
    items = r['items']
    for item in items:
        volume_info = item['volumeInfo']

        title = volume_info.get('title', None)
        publish_date = volume_info.get('publishedDate', None)
        language = volume_info.get('language', None)
        page_count = volume_info.get('pageCount', None)

        authors = None
        isbn = None
        thumbnail = None

        if volume_info.get('authors'):
            authors = ", ".join(volume_info['authors'])

        if volume_info.get("industryIdentifiers"):
            industry_identifiers = volume_info["industryIdentifiers"]
            for industry_identifier in industry_identifiers:
                if industry_identifier['type'] == 'ISBN_13':
                    isbn = industry_identifier['identifier']

        if volume_info.get('imageLinks'):
            thumbnail = volume_info['imageLinks']['thumbnail']

        book = Book(title=title, authors=authors, publish_date=publish_date, isbn=isbn, page_count=page_count,
                    thumbnail=thumbnail, language=language)

        if not book.is_in_database():
            book.save()


def normalize_date(date):
    date = date.replace("/", "-")
    date = date.replace(".", "-")
    date = date.replace("\\", "-")
    date_list = date.split("-")
    if len(date_list) == 1:
        return date
    if int(date_list[0]) < int(date_list[-1]):
        date_list.reverse()
        date = "-".join(date_list)

    return date


def normalize_language(language):
    if len(language) == 2:
        return language.lower()
    else:
        return check_name(language)


def filter_books(title, authors, language, date_begin, date_end):
    books = Book.objects.all()

    if title:
        books = books.filter(title__icontains=title)

    if authors:
        books = books.filter(authors__icontains=authors)

    if language:
        language = normalize_language(language)
        books = books.filter(language=language)

    if date_begin:
        books = [book for book in books if book.publish_date > date_begin]

    if date_end:
        books = [book for book in books if book.publish_date < date_end]

    return books
