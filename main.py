import psycopg2
from hh_api import HH_vacancy
from db_manager import DBManager
import json
from config import config

params = config()
hh_api = HH_vacancy()
vacancy_list = hh_api.get_vacancy()
hh_api.drop_database("hh_vacancies")
hh_api.create_database("hh_vacancies")
hh_api.create_tables()
hh_api.insert_values_employee(vacancy_list)
hh_api.insert_values_vacancies(vacancy_list)
db_manager = DBManager()
db_manager.get_all_vacancies()
db_manager.get_vacancies_with_higher_salary()
db_manager.get_avg_salary()
db_manager.get_vacancies_with_keyword("программист")
db_manager.get_companies_and_vacancies_count()
