# import psycopg2
from hh_api import HH_vacancy
from db_manager import DBManager
from config import config
import pprint

params = config()
hh_api = HH_vacancy()
vacancy_list = hh_api.get_vacancy()
hh_api.drop_database("hh_vacancies")
hh_api.create_database("hh_vacancies")
hh_api.create_tables()
hh_api.insert_values_employee(vacancy_list)
hh_api.insert_values_vacancies(vacancy_list)

db_manager = DBManager()
print(db_manager.get_all_vacancies())
pprint.pprint(db_manager.get_vacancies_with_higher_salary())
print(db_manager.get_avg_salary())
pprint.pprint(db_manager.get_vacancies_with_keyword('бухгалтер'))
pprint.pprint(db_manager.get_companies_and_vacancies_count())
# pprint.pprint(result)
