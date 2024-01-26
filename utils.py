import requests
import psycopg2


employer_ids = [
    "3127",  # Мегафон
    "3529",  # Сбербанк
    "78638",  # Тинькофф
    "1740",  # Яндекс
    "2748",  # Ростелеком
    "3776",  # МТС
    "2180",  # Ozon
    "1122462",  # Skyeng
    "15478",  # Вконтакте
    "84585"  # Авито
]


def get_vacancy():
    vacancy_list = []
    for employer_id in employer_ids:
        params = {"employer_id": employer_id,
                  "per_page": 100,
                  "only_with_salary": True,
                  }
        hh_url = "https://api.hh.ru/vacancies"
        response = requests.get(hh_url, params)
        if response.status_code == 200:
            vacancies = response.json()
            for item in vacancies["items"]:
                if item["salary"]["from"]:
                    vacancy_list.append(item)
        return vacancy_list


def drop_database(params):
    conn = psycopg2.connect(dbname="postgres", **params)
    with conn.cursor() as cur:
        conn.autocommit = True
        cur.execute(f'drop database if exists hh_vacancies')


def create_database(params):
    conn = psycopg2.connect(dbname="postgres", **params)
    with conn.cursor() as cur:
        conn.autocommit = True
        cur.execute(f'create database hh_vacancies')
    conn.commit()
    conn.close()


def create_tables(params):
    conn = psycopg2.connect(dbname="hh_vacancies", **params)
    with conn.cursor() as cur:
        conn.autocommit = True
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
        conn.commit()
        conn.close()


def insert_values_employee(params, vacancy_list):
    conn = psycopg2.connect(dbname="hh_vacancies", **params)
    with conn.cursor() as cur:
        conn.autocommit = True
        for vacancy in vacancy_list:
            cur.execute(f'''insert into employers(employer_id, employer_name, employer_url)
                      VALUES( %s, %s, %s) on conflict do nothing''',
                        (vacancy['employer']['id'], vacancy['employer']['name'],
                         vacancy['employer']['url']))
    conn.commit()
    conn.close()


def insert_values_vacancies(params, vacancy_list):
    conn = psycopg2.connect(dbname="hh_vacancies", **params)
    with conn.cursor() as cur:
        conn.autocommit = True
        for vacancy in vacancy_list:
            cur.execute(f'''insert into vacancies(vacancy_id, city, employer_name, 
                                                  vacancy_name, salary_min, vacancy_url) 
                VALUES( %s, %s, %s, %s, %s, %s) on conflict do nothing''', (vacancy['id'],
                                                                            vacancy['area']['name'],
                                                                            vacancy['employer']['name'],
                                                                            vacancy['name'],
                                                                            vacancy['salary']['from'],
                                                                            vacancy['alternate_url']))
    conn.commit()
    conn.close()
