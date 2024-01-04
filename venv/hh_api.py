import requests
import json


employer_ids =[
    "3127",  # Мегафон
    "3529",  # Сбер
    "78638",  # Тинькофф
    "1740",  # Яндекс
    "2748",  # Ростелеком
    "3776",  # МТС
    "2180",  # Ozon
    "1122462",  # Skyeng
    "15478",  # VK
    "84585"  # Авито
]
class HH_vacancy():
    """Класс для работы с API платформы HeadHunter"""

    HH_URL = "https://api.hh.ru/vacancies"
    HH_COMPANY = "https://api.hh.ru/employers"
    HH_AREAS = "https://api.hh.ru/suggests/areas"
    company_id = "id_companies.json"

    # def get_company_id(self):
    #     company_id_list = []
    #     with open(self.company_id, encoding="utf-8") as file:
    #         company_json = json.load(file)
    #         for company in company_json:
    #             company_id_list.append(company['id'])
    #     return company_id_list
    #
    #
    # def get_company_name(self):
    #     company_name_list = []
    #     with open(self.company_id, encoding="utf-8") as file:
    #         company_json = json.load(file)
    #         for company in company_json:
    #             company_name_list.append(company['name'])
    #     return company_name_list


    def get_vacancy(self):
        """Получение данных о вакансиях работодателя"""
        vacancy_list = []
        for employer_id in employer_ids:
            params = {"employer_id": employer_id,
                      "per_page": 100,
                      "only_with_salary": True,
                      }
            response = requests.get(self.HH_URL, params)
            if response.status_code == 200:
                vacancies = response.json()
                for item in vacancies["items"]:
                    if item["salary"]["from"]:
                        vacancy_list.append(item)
        for vacancy in vacancy_list:
            print(vacancy)

hh = HH_vacancy()
hh.get_vacancy()
