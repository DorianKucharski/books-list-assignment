from django.db import models
from django.db.models import Q


class Book(models.Model):
    db_table = "books"

    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=100, default=None, blank=True, null=True)
    publish_date = models.CharField(max_length=100)
    isbn = models.IntegerField(default=None, blank=True, null=True)
    page_count = models.IntegerField(default=None, blank=True, null=True)
    thumbnail = models.CharField(max_length=999, default=None, blank=True, null=True)
    language = models.CharField(max_length=100)

    def __str__(self):
        return " | ".join([self.title])

    def update_by_other_object(self, other):
        self.title = other.title
        self.authors = other.authors
        self.publish_date = other.publish_date
        self.isbn = other.isbn
        self.page_count = other.page_count
        self.thumbnail = other.thumbnail
        self.language = other.language

    def is_in_database(self):
        found = Book.objects.filter(Q(title=self.title) & Q(authors=self.authors) & Q(publish_date=self.publish_date)
                                    & Q(isbn=self.isbn) & Q(page_count=self.page_count) & Q(thumbnail=self.thumbnail)
                                    & Q(language=self.language))
        return len(found) > 0
