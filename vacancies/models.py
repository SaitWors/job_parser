# vacancies/models.py

from django.db import models

class Vacancy(models.Model):
    hh_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    salary_from = models.FloatField(null=True, blank=True)
    salary_to = models.FloatField(null=True, blank=True)
    working_days = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)  # Ссылка на объявление

    def __str__(self):
        return self.name
