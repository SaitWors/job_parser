from django.shortcuts import render, redirect
from django.views import View
from django.core.management import call_command
from django.http import JsonResponse
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
        elif filter_type == 'working_days':
            vacancies = vacancies.filter(working_days__icontains=value)
        elif filter_type == 'id':
            vacancies = vacancies.filter(hh_id__icontains=value)

    total_vacancies = vacancies.count()
    return render(request, 'vacancies/job_list.html', {
        'vacancies': vacancies,
        'filter_type': filter_type,
        'value': value,
        'total_vacancies': total_vacancies
    })

class RunParseVacanciesCommandView(View):
    def post(self, request, *args, **kwargs):
        filter_type = request.POST.get('filter', '')
        filter_value = request.POST.get('value', '')
        pages = request.POST.get('pages', '1')

        try:
            pages = int(pages)  # Преобразование в целое число
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid number of pages'}, status=400)

        call_command('parse_vacancies', filter=filter_type, value=filter_value, pages=pages)
        
        total_vacancies = Vacancy.objects.count()
        return JsonResponse({'status': 'success', 'total_vacancies': total_vacancies})

    def get(self, request, *args, **kwargs):
        filter_type = request.GET.get('filter', '')
        filter_value = request.GET.get('value', '')
        vacancies = Vacancy.objects.all()

        if filter_type and filter_value:
            if filter_type == 'name':
                vacancies = vacancies.filter(name__icontains=filter_value)
            elif filter_type == 'salary':
                try:
                    filter_value = int(filter_value)
                    vacancies = vacancies.filter(salary_from__gte=filter_value)
                except ValueError:
                    pass
            elif filter_type == 'working_days':
                vacancies = vacancies.filter(working_days__icontains=filter_value)
            elif filter_type == 'id':
                vacancies = vacancies.filter(hh_id__icontains=filter_value)

        total_vacancies = vacancies.count()
        context = {
            'vacancies': vacancies,
            'filter_type': filter_type,
            'value': filter_value,
            'total_vacancies': total_vacancies,
        }
        return render(request, 'vacancies/job_list.html', context)
