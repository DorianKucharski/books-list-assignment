# Generated by Django 3.2.3 on 2021-09-15 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_list', '0005_auto_20210914_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
