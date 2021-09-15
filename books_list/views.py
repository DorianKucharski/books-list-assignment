import datetime
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm, ImportForm
from .utils import normalize_language, get_books_from_api, filter_books
from .serializers import BookSerializer


def books_list(request):
    title = request.GET.get('title', "")
    authors = request.GET.get('authors', "")
    language = request.GET.get('language', "")
    date_begin = request.GET.get('date_begin', None)
    date_end = request.GET.get('date_end', None)
    books = filter_books(title, authors, language, date_begin, date_end)

    data = {'books': books, 'title': title, 'authors': authors, 'language': language, 'date_begin': date_begin,
            'date_end': date_end}

    return render(request, "list.html", data)


def book_edit(request, book_id):
    if int(book_id) > 0:
        book = Book.objects.get(id=book_id)
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                new_book = form.to_book()
                book.update_by_other_object(new_book)
                book.save()
                return redirect('/')
        else:
            book_form = BookForm.from_book(book)
            return render(request, "book.html", {"form": book_form})
    else:
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                if not Book.objects.filter(Q(title=form.data['title']) & Q(authors=form.data['authors'])):
                    form.to_book().save()
                return redirect('/')
        else:
            form = BookForm()

        return render(request, "book.html", {"form": form})


def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/')


def book_import(request):
    if request.method == 'GET':
        form = ImportForm()
        return render(request, "import.html", {'form': form})
    else:
        form = BookForm(request.POST)
        data = form.data.copy()
        del data['csrfmiddlewaretoken']
        data = {k: v for k, v in data.items() if v}
        query = "+".join([":".join([k, v]) for k, v in data.items()])
        get_books_from_api(query)
        return redirect('/')


def api(request):
    title = request.GET.get('title', None)
    authors = request.GET.get('authors', None)
    language = request.GET.get('language', None)
    date_begin = request.GET.get('date_begin', None)
    date_end = request.GET.get('date_end', None)
    books = filter_books(title, authors, language, date_begin, date_end)
    info = "query string parameters: title, authors, language, date_begin, date_end"
    example = "https://books-list-assignment.herokuapp.com/api?authors=tolkien&date_begin=2000-01-01"

    response = {'info': info, 'example': example, 'books': [BookSerializer(o).data for o in books]}
    return JsonResponse(response)
