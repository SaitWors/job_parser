import requests
from django.core.management.base import BaseCommand
from vacancies.models import Vacancy

class Command(BaseCommand):
    help = 'Парсинг вакансий с HH.ru и сохранение в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('--filter', type=str, help='Фильтрация вакансий по имени или зарплате')
        parser.add_argument('--value', type=str, help='Значение для фильтра')
        parser.add_argument('--pages', type=int, default=1, help='Количество страниц для парсинга')

    def handle(self, *args, **options):
        def get_vacancies(filter_type, filter_value, pages=1):
            res = []
            for page in range(pages):
                params = {
                    'text': f'{filter_value}',
                    'page': page,
                    'per_page': 52,
                    'only_with_salary': 'true' if filter_type == 'salary' else 'false',
                }
                req = requests.get('https://api.hh.ru/vacancies', params=params).json()
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
        total_vacancies = len(vacancies_data)

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
            print(f"ID: {vac['id']}")
            print(f"Название: {vac['name']}")
            print(f"Ссылка на профиль: {vac['alternate_url']}")
            print(f"Зарплата от: {vac['salary']['from'] if vac['salary'] else 'N/A'}")
            print(f"Зарплата до: {vac['salary']['to'] if vac['salary'] else 'N/A'}")
            print(f"Рабочие дни: {vac['schedule']['name'] if 'schedule' in vac else 'N/A'}")
            print('-' * 40)

        self.stdout.write(self.style.SUCCESS(f'Данные собраны и отфильтрованы. Обработано {total_vacancies} вакансий.'))