from django.urls import path
from . import views

from .views import RunParseVacanciesCommandView

urlpatterns = [
    path('', views.vacancy_list, name='vacancy_list'),
    path('run-parse-vacancies/', RunParseVacanciesCommandView.as_view(), name='run_parse_vacancies'),
]
