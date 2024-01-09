import requests
import psycopg2


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
    # HH_COMPANY = "https://api.hh.ru/employers"
    # HH_AREAS = "https://api.hh.ru/suggests/areas"
    # company_id = "id_companies.json"

    def __init__(self, user: str="postgres", password: str="1967", host: str ='localhost', port: str ='5432'):
        self.conn = psycopg2.connect(user=user, password=password, host=host, port=port)

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
        """Получение данных о вакансиях работодателя с платформы HeadHunter в json-формате"""
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
        return vacancy_list
        # for vacancy in vacancy_list:
        #    print(vacancy)

    def drop_database(self, db_name):
        with self.conn.cursor() as cur:
            self.conn.autocommit=True
            cur.execute(f'drop database if exists {db_name}')


    def create_database(self, db_name):
        with self.conn.cursor() as cur:
            self.conn.autocommit = True
            cur.execute(f'create database {db_name}')


    def create_tables(self):
        with self.conn.cursor() as cur:
            self.conn.autocommit = True
            cur.execute(f'''create table if not exists employers(
            employer_id INTEGER primary key, 
            employer_name VARCHAR(100) NOT NULL, 
            employer_url VARCHAR(50))''')

            cur.execute(f'''create table if not exists vacancies(
                vacancy_id INTEGER PRIMARY KEY,
                employer_id INTEGER, 
                employer_name VARCHAR(100) NOT NULL,
                city varchar(50),
                vacancy_name VARCHAR(100) NOT NULL,
                salary_min INTEGER,
                vacancy_url VARCHAR(50),
                CONSTRAINT fk_employers_employer_id FOREIGN KEY(employer_id) 
                                REFERENCES employers(employer_id)
                )''')


    def insert_values_employee(self, vacancy_list):
        with self.conn.cursor() as cur:
            self.conn.autocommit = True
            for vacancy in vacancy_list:
                cur.execute(f'''insert into employers(employer_id, employer_name, employer_url)
                          VALUES( %s, %s, %s) on conflict do nothing''',
                            (vacancy['employer']['id'], vacancy['employer']['name'], vacancy['employer']['url']))



    def insert_values_vacancies(self, vacancy_list):
        with self.conn.cursor() as cur:
            self.conn.autocommit = True
            for vacancy in vacancy_list:
                cur.execute(f'''insert into vacancies(vacancy_id, city, employer_name, 
                                                     vacancy_name, salary_min, vacancy_url) 
                VALUES( %s, %s, %s, %s, %s, %s) on conflict do nothing''', (vacancy['id'], vacancy['area']['name'],
                                                         vacancy['employer']['name'], vacancy['name'],
                                                         vacancy['salary']['from'],
                                                         vacancy['alternate_url']))
