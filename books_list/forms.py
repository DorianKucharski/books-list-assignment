from django import forms
from books_list.validation import date_validator, isbn_validator, url_validator, language_validator
from books_list.models import Book
from books_list.utils import normalize_language, normalize_date


class BookForm(forms.Form):
    widget = forms.TextInput(attrs={'class': 'form-control'})
    title = forms.CharField(max_length=100, widget=widget)
    authors = forms.CharField(max_length=100, widget=widget, required=False)
    publish_date = forms.CharField(max_length=100, widget=widget, validators=[date_validator])
    isbn = forms.IntegerField(widget=widget, required=False, validators=[isbn_validator])
    page_count = forms.IntegerField(widget=widget, required=False)
    thumbnail = forms.CharField(max_length=999, widget=widget, required=False, validators=[url_validator])
    language = forms.CharField(max_length=100, widget=widget, validators=[language_validator])

    def to_book(self):
        book = Book(title=self.data['title'],
                    publish_date=normalize_date(self.data['publish_date']),
                    language=normalize_language(self.data['language']))

        if self.data['authors']:
            book.authors = self.data['authors']

        if self.data['isbn']:
            book.isbn = self.data['isbn']

        if self.data['page_count']:
            book.page_count = self.data['page_count']

        if self.data['thumbnail']:
            book.thumbnail = self.data['thumbnail']

        return book

    @staticmethod
    def from_book(book):
        book_form = BookForm(data={'title': book.title, 'authors': book.authors, 'publish_date': book.publish_date,
                                      'isbn': book.isbn, 'page_count': book.page_count, 'thumbnail': book.thumbnail,
                                      'language': book.language})

        return book_form


class ImportForm(forms.Form):
    widget = forms.TextInput(attrs={'class': 'form-control'})
    intitle = forms.CharField(max_length=100, widget=widget, required=False)
    inauthor = forms.CharField(max_length=100, widget=widget, required=False)
    inpublisher = forms.CharField(max_length=100, widget=widget, required=False)
    subject = forms.CharField(max_length=100, widget=widget, required=False)
    isbn = forms.CharField(max_length=100, widget=widget, required=False)
    lccn = forms.CharField(max_length=100, widget=widget, required=False)
    oclc = forms.CharField(max_length=100, widget=widget, required=False)
