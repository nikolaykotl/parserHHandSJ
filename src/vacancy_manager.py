import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy
import os

class VacancyManager(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy_obj):
        """
        Абстрактный метод для добавления вакансии.
        """
        pass

    @abstractmethod
    def get_vacancies(self):
        """
        Абстрактный метод для получения списка вакансий.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_obj):
        """
        Абстрактный метод для удаления вакансии.
        """
        pass

    @abstractmethod
    def filter_vacancies(self, params):
        """
        Абстрактный метод для фильтрации вакансий.
        """
        pass

class JSONSaver(VacancyManager):

    def __init__(self):
        self.vacancies = []

    def file_exists(self):
        if not os.path.exists('vacancies.json') or not os.path.getsize('vacancies.json'):
            raise FileNotFoundError('Файл с вакансиями пуст или не существует.')

    def add_vacancy(self, vacancy_obj):
        if os.path.exists('vacancies.json') and os.path.getsize('vacancies.json'):
            with open('vacancies.json', encoding='utf8') as file:
                vc_list = json.load(file)
        else:
            vc_list = []

        vc_list.append(vacancy_obj)

        with open('vacancies.json', 'w', encoding='utf8') as file:
            json.dump(vc_list, file, ensure_ascii=False)

    def get_vacancies(self):
        self.file_exists()

        with open('vacancies.json', encoding='utf8') as file:
            vc_list = json.load(file)

            self.vacancies = [Vacancy(vc) for vc in vc_list]
            return self.vacancies

    def filter_vacancies(self, params):
        if params is None:
            raise ValueError('Необходимо указать ключевое слово для поиска.')
        if len(params) == 0:
            raise ValueError('Фильтрация пробела недопустима.')

        params_lower = [param.lower() if isinstance(param, str) else param for param in params]

        filtered_vacancies = []

        for vc in self.vacancies:
            vc_attrs = [vc.name.lower(), vc.experience.lower(), str(vc.salary_from), str(vc.salary_to), vc.sity.lower()]
            if any(param in attr for param in params_lower for attr in vc_attrs):
                filtered_vacancies.append(vc)

        self.vacancies = filtered_vacancies
        return self.vacancies

    def sort_vacancies_by_salary(self):
        sorted_vacancies = sorted(self.vacancies, key=lambda vc: max(vc.salary_from or 0, vc.salary_to or 0), reverse=True)

        self.vacancies = sorted_vacancies
        return self.vacancies

    def salary_top(self, top_n):
        if len(self.sort_vacancies_by_salary()) <= top_n:
            return self.sort_vacancies_by_salary()
        else:
            return self.sort_vacancies_by_salary()[:top_n]
    def delete_vacancy(self, vacancy_obj):

        self.file_exists()

        with open('vacancies.json', 'w', encoding='utf8') as file:
            pass
