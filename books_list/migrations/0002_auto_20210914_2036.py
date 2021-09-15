# Generated by Django 3.2.3 on 2021-09-14 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_list', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='pages',
            new_name='page_count',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='cover',
            new_name='thumbnail',
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.CharField(max_length=100),
        ),
    ]
