from django.test import TestCase
from .validation import url_validator, isbn_validator, date_validator, language_validator
from django.core.exceptions import ValidationError
from .models import Book
from .forms import BookForm


class ValidationTests(TestCase):
    def validation_test(self, validator, value, correct):
        try:
            validator(value)
        except ValidationError:
            self.assertTrue(not correct)
        else:
            self.assertTrue(correct)

    def test_url_validation_valid(self):
        self.validation_test(url_validator, "http://google.pl", True)

    def test_url_validation_not_valid(self):
        self.validation_test(url_validator, "google.pl", False)

    def test_isbn_validation_valid(self):
        self.validation_test(isbn_validator, 1234567890123, True)

    def test_isbn_validation_not_valid(self):
        self.validation_test(isbn_validator, 123456789, False)

    def test_date_validation_valid11(self):
        self.validation_test(date_validator, "01-01-2010", True)

    def test_date_validation_valid21(self):
        self.validation_test(date_validator, "01.01.2010", True)

    def test_date_validation_valid31(self):
        self.validation_test(date_validator, "01/01/2010", True)

    def test_date_validation_valid12(self):
        self.validation_test(date_validator, "2010-01-01", True)

    def test_date_validation_valid22(self):
        self.validation_test(date_validator, "2010.01.01", True)

    def test_date_validation_valid32(self):
        self.validation_test(date_validator, "2010/01/01", True)

    def test_date_validation_not_valid1(self):
        self.validation_test(date_validator, "2030/01/01", False)

    def test_date_validation_not_valid2(self):
        self.validation_test(date_validator, "2030/01/01/54", False)

    def test_language_validation_valid1(self):
        self.validation_test(language_validator, "pl", True)

    def test_language_validation_valid2(self):
        self.validation_test(language_validator, "PL", True)

    def test_language_validation_valid3(self):
        self.validation_test(language_validator, "polish", True)

    def test_language_validation_valid4(self):
        self.validation_test(language_validator, "PoLiSh", True)

    def test_language_validation_not_valid1(self):
        self.validation_test(language_validator, "PoLisz", False)

    def test_language_validation_not_valid2(self):
        self.validation_test(language_validator, "xx", False)


class BookFormsBooksTests(TestCase):
    def test_form_to_book(self):
        title = 'title'
        authors = 'authors'
        publish_date = '2010-10-10'
        isbn = 1234567890123
        page_count = 999
        thumbnail = "https://google.com"
        language = "en"

        book_form = BookForm(data={'title': title, 'authors': authors, 'publish_date': publish_date,
                                   'isbn': isbn, 'page_count': page_count, 'thumbnail': thumbnail,
                                   'language': language})

        book = book_form.to_book()

        self.assertEqual(title, book.title)
        self.assertEqual(authors, book.authors)
        self.assertEqual(publish_date, book.publish_date)
        self.assertEqual(isbn, book.isbn)
        self.assertEqual(page_count, book.page_count)
        self.assertEqual(thumbnail, book.thumbnail)
        self.assertEqual(language, book.language)

    def test_book_to_form(self):
        title = 'title'
        authors = 'authors'
        publish_date = '2010-10-10'
        isbn = 1234567890123
        page_count = 999
        thumbnail = "https://google.com"
        language = "en"

        book = Book(title=title, authors=authors, publish_date=publish_date, isbn=isbn, page_count=page_count,
                    thumbnail=thumbnail, language=language)

        book_form = BookForm.from_book(book)

        self.assertEqual(title, book_form.data['title'])
        self.assertEqual(authors, book_form.data['authors'])
        self.assertEqual(publish_date, book_form.data['publish_date'])
        self.assertEqual(isbn, book_form.data['isbn'])
        self.assertEqual(page_count, book_form.data['page_count'])
        self.assertEqual(thumbnail, book_form.data['thumbnail'])
        self.assertEqual(language, book_form.data['language'])


class ApiTests(TestCase):
    def setUp(self):
        Book.objects.create(title="title", authors="english", publish_date="2000-01-01", language="en")
        Book.objects.create(title="tytul", authors="polish", publish_date="2005-01-01", language="pl")
        Book.objects.create(title="titel", authors="german", publish_date="2010-01-01", language="en")
        Book.objects.create(title="titre", authors="german", publish_date="2015-01-01", language="en")

    def test_get_all(self):
        response = self.client.get("/api").json()
        books = response['books']
        self.assertEqual(len(books), 4)
        self.assertEqual(books[0]['title'], 'title')
        self.assertEqual(books[1]['title'], 'tytul')
        self.assertEqual(books[2]['title'], 'titel')
        self.assertEqual(books[3]['title'], 'titre')

    def test_filter_by_language(self):
        response = self.client.get("/api?language=en").json()
        books = response['books']
        self.assertEqual(len(books), 3)
        self.assertEqual(books[0]['title'], 'title')
        self.assertEqual(books[1]['title'], 'titel')
        self.assertEqual(books[2]['title'], 'titre')

    def test_filter_by_authors(self):
        response = self.client.get("/api?authors=german").json()
        books = response['books']
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]['title'], 'titel')
        self.assertEqual(books[1]['title'], 'titre')

    def test_filter_by_date(self):
        response = self.client.get("/api?date_begin=2012-01-01").json()
        books = response['books']
        self.assertEqual(len(books), 1)

    def test_filter_by_date_and_language(self):
        response = self.client.get("/api?date_begin=2004-01-01&date_end=2012-01-01&language=en").json()
        books = response['books']
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], 'titel')





