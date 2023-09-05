import math
import os
from abc import ABC, abstractmethod
import requests
import dotenv

class VacancyEngine(ABC):
    """
    Абстрактный класс для работы с API сайтов вакансий
    """
    @abstractmethod
    def get_vacancies(self):
        """
        Получение вакансий с использованием API.
        """
        pass

    @abstractmethod
    def get_formatted_vacancies(self):
        """
        Получение отформатированных данных о вакансиях.
        """
        pass


class HeadHunterAPI(VacancyEngine):
    url = f"https://api.hh.ru/vacancies"

    def __init__(self, keyword):
        self.quantity = None
        self.vacancies = []
        self.params = {
            "page": 1,
            "per_page": 100,
            "text": keyword,
            "archived": False
        }

    def get_vacancies(self, quantity):

        pages_count = math.ceil(quantity / self.params["per_page"])
        self.quantity = quantity
        self.vacancies = []

        response = requests.get(self.url, params=self.params)

        if response.status_code != 200:
            raise print(f"Ошибка получения вакансий! Статус {response.status_code}")

        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page

            if self.quantity <= 100:
                self.params["per_page"] = self.quantity
                response = requests.get(self.url, params=self.params)
                page_vacancies = response.json()["items"]
            else:
                self.params["per_page"] = 100
                response = requests.get(self.url, params=self.params)
                page_vacancies = response.json()["items"]

            self.vacancies.extend(page_vacancies)
            self.quantity -= self.params["per_page"]
            if len(page_vacancies) == 0:
                break
        print(f"Получено вакансий с платформы {self.__class__.__name__}: {len(self.vacancies)}.")

    def get_formatted_vacancies(self):
        formatted_vacancies = []

        for vacancy in self.vacancies:
            salary = vacancy["salary"]

            formatted_vacancy = {
                "name": vacancy["name"],
                "experience": vacancy["experience"]["name"],
                "salary_from": salary["from"] if salary and salary["from"] != 0 else None,
                "salary_to": salary["to"] if salary and salary["to"] != 0 else None,
                "currency": salary["currency"] if salary and salary["currency"] else None,
                "sity": vacancy["area"]["name"],
                "employer": vacancy["employer"]["name"],
                "url": vacancy["alternate_url"],
            }
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies

class SuperJobAPI(VacancyEngine):
    url = f'https://api.superjob.ru/2.0/vacancies'

    def __init__(self, keyword):
        self.quantity = None
        self.vacancies = []

        self.params = {
            "page": None,
            "count": 100,
            "keyword": keyword,
            "archive": False
        }
        dotenv.load_dotenv()
        X_Api_App_Id = os.getenv('X_Api_App_Id')
        Authorization = os.getenv('Authorization')
        self.headers = {
            'X-Api-App-Id': X_Api_App_Id,
            'Authorization': Authorization
        }

    def get_vacancies(self, quantity):
        pages_count = math.ceil(quantity / self.params["count"])
        self.quantity = quantity
        if quantity < 100:
            self.params["count"] = quantity
        else:
            self.params["count"] = 100
        self.vacancies = []

        response = requests.get(self.url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            raise f'Запрос не выполнен с кодом состояния: {response.status_code}'

        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page

            if self.quantity <= 100:
                self.params["count"] = self.quantity
                response = requests.get(self.url, params=self.params, headers=self.headers)
                page_vacancies = response.json().get("objects",[])
            else:
                self.params["count"] = 100
                response = requests.get(self.url, params=self.params, headers=self.headers)
                page_vacancies = response.json().get("objects", [])

            self.vacancies.extend(page_vacancies)
            self.quantity -= self.params["count"]

            if len(page_vacancies) == 0:
                break
        print(f"Загружено вакансий с платформы {self.__class__.__name__}: {len(self.vacancies)}")


    def get_formatted_vacancies(self):
        formatted_vacancies = []

        for vacancy in self.vacancies:

            formatted_vacancy = {
                "name": vacancy["profession"],
                "experience": vacancy["experience"]["title"],
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] != 0 else None,
                "currency": vacancy["currency"],
                "sity": vacancy["town"]["title"],
                "employer": vacancy["firm_name"],
                "url": vacancy["link"],
            }
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies
