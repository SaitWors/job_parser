# vacancies/views.py

from django.shortcuts import render
from .models import Vacancy

def vacancy_list(request):
    filter_type = request.GET.get('filter')
    value = request.GET.get('value')
    vacancies = Vacancy.objects.all()

    if filter_type and value:
        if filter_type == 'name':
            vacancies = vacancies.filter(name__icontains=value)
        elif filter_type == 'salary':
            try:
                salary_value = float(value)
                vacancies = vacancies.filter(salary_from__lte=salary_value, salary_to__gte=salary_value)
            except ValueError:
                pass  # Неверное значение зарплаты

    return render(request, 'vacancies/vacancy_list.html', {'vacancies': vacancies, 'filter_type': filter_type})

