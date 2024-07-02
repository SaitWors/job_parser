import requests
from django.core.management.base import BaseCommand
from vacancies.models import Vacancy

class Command(BaseCommand):
    help = 'Parse vacancies from HH.ru and save to database'

    def add_arguments(self, parser):
        parser.add_argument('--filter', type=str, help='Filter vacancies by name or salary')
        parser.add_argument('--value', type=str, help='Value for the filter')
        parser.add_argument('--pages', type=int, default=1, help='Number of pages to parse')

    def handle(self, *args, **options):
        def get_vacancies(filter_type, filter_value, pages=1):
            res = []
            for page in range(pages):
                params = {
                    'text': f'{filter_value}',
                    'page': page,
                    'per_page': 100,
                    'only_with_salary': 'true' if filter_type == 'salary' else 'false',
                }
                req = requests.get('https://api.hh.ru/vacancies', params).json()
                if 'items' in req.keys():
                    res.extend(req['items'])
                print('|', end='')
            return res

        # Получение параметров
        filter_type = options['filter']
        filter_value = options['value']
        pages = options['pages']

        # Сбор данных о вакансиях
        vacancies_data = get_vacancies(filter_type, filter_value, pages)

        # Сохранение данных в базу данных
        new_vacancies = 0
        for vac in vacancies_data:
            _, created = Vacancy.objects.update_or_create(
                hh_id=vac['id'],
                defaults={
                    'name': vac['name'],
                    'salary_from': vac['salary']['from'] if vac['salary'] else None,
                    'salary_to': vac['salary']['to'] if vac['salary'] else None,
                    'working_days': vac['schedule']['name'] if 'schedule' in vac else '',
                    'url': vac['alternate_url']
                }
            )
            if created:
                new_vacancies += 1

        self.stdout.write(self.style.SUCCESS(f'Data collected and filtered. {new_vacancies} new vacancies added.'))



##

class Command(BaseCommand):
    help = 'Parse vacancies from HH.ru and save to database'

    def add_arguments(self, parser):
        parser.add_argument('--filter', type=str, help='Filter vacancies by name or salary')
        parser.add_argument('--value', type=str, help='Value for the filter')
        parser.add_argument('--pages', type=int, default=1, help='Number of pages to parse')

    def handle(self, *args, **options):
        def get_vacancies(filter_type, filter_value, pages=1):
            res = []
            for page in range(pages):
                params = {
                    'text': f'{filter_value}',
                    'page': page,
                    'per_page': 100,
                    'only_with_salary': 'true' if filter_type == 'salary' else 'false',
                }
                req = requests.get('https://api.hh.ru/vacancies/', params).json()
                if 'items' in req.keys():
                    res.extend(req['items'])
                print('|', end='')
            return res

        # Получение параметров
        filter_type = options['filter']
        filter_value = options['value']
        pages = options['pages']

        # Сбор данных о вакансиях
        vacancies_data = get_vacancies(filter_type, filter_value, pages)
        total_vacancies = len(vacancies_data)  # Подсчет количества вакансий

        # Сохранение данных в базу данных
        for vac in vacancies_data:
            Vacancy.objects.update_or_create(
                hh_id=vac['id'],
                defaults={
                    'name': vac['name'],
                    'salary_from': vac['salary']['from'] if vac['salary'] else None,
                    'salary_to': vac['salary']['to'] if vac['salary'] else None,
                    'working_days': vac['schedule']['name'] if 'schedule' in vac else '',
                    'url': vac['alternate_url']
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Data collected and filtered. Total vacancies: {total_vacancies}'))