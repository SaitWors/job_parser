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


from django.shortcuts import redirect
from django.views import View
from django.core.management import call_command
from django.http import JsonResponse

class RunParseVacanciesCommandView(View):
    def post(self, request, *args, **kwargs):
        filter_type = request.POST.get('filter', '')
        filter_value = request.POST.get('value', '')
        pages = request.POST.get('pages', '1')

        try:
            pages = int(pages)  # Преобразование в целое число
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid number of pages'}, status=400)

        # Запуск команды
        call_command('parse_vacancies', filter=filter_type, value=filter_value, pages=pages)

        # Перенаправление на страницу с обновленными данными
        return redirect('vacancy_list')

from django.views.generic import ListView
from .models import Vacancy

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_type = self.request.GET.get('filter')
        value = self.request.GET.get('value')

        if filter_type and value:
            if filter_type == 'name':
                queryset = queryset.filter(name__icontains=value)
            elif filter_type == 'salary':
                queryset = queryset.filter(salary_from__gte=value)  # Или любой другой фильтр по зарплате

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_type'] = self.request.GET.get('filter', '')
        context['value'] = self.request.GET.get('value', '')
        return context
    



##
from django.shortcuts import render
from django.views import View
from django.core.management import call_command
from django.http import JsonResponse
from .models import Vacancy

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

        total_vacancies = vacancies.count()

        context = {
            'vacancies': vacancies,
            'filter_type': filter_type,
            'value': filter_value,
            'total_vacancies': total_vacancies,
        }
        return render(request, 'vacancies/vacancy_list.html', context)