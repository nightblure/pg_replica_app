from django.db import models

"""
миграции:
    python manage.py makemigrations
    python manage.py migrate --database=master
    python manage.py migrate --database=replica
"""


class Item(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
