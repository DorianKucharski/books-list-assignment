from django.urls import path
from books_list import views

urlpatterns = [
    path('', views.books_list),
    path('<int:book_id>/', views.book_edit),
    path('delete/<int:book_id>/', views.book_delete),
    path('import', views.book_import),
    path('api', views.api)
]