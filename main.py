from hh_api import Api_client
from db_manager import DBManager
from config import config
import pprint


params = config()
db_name = "hh_vacancies"
api_client = Api_client(db_name, params)
vacancy_list = api_client.get_vacancy()
api_client.drop_database()
api_client.create_database()
api_client.create_tables()
api_client.insert_values_employee(vacancy_list)
api_client.insert_values_vacancies(vacancy_list)
db_manager = DBManager("hh_vacancies", params)
print("""Добрый день. Предлагаем вам найти вакансии с сайта Head Hunter у следующий кампаний: 
Мегафон (3127), Сбербанк (3529), Тинькоф (78638), Яндекс (1740), Ростелеком (2748), МТС (3776), 
Озон(2180), Skyeng (1122462), Вконтакте (15478), Авито (84585).""")
while True:
    index = input("""Нажмите следующую цифру, если вы хотите: 
                      - вывести список всех полученных вакансий - "1";
                      - вывести список вакансий с зарплатой выше средней - "2";
                      - вывести среднюю зарплату по найденным вакансиям - "3";
                      - вывести список вакансий по заданному слову поиска - "4";
                      - вывести список кампаний и количество найденных вакансий - "5";
                      - завершить работу программы - "0"
                      """)
    if index == "0":
        print("Работа программы завершена")
        break
    elif index == "1":
        all_vacancies = db_manager.get_all_vacancies()
        for vacancy in all_vacancies:
            print(vacancy)
    elif index == "2":
        all_vacancies1 = db_manager.get_vacancies_with_higher_salary()
        for vacancy in all_vacancies1:
            print(vacancy)
    elif index == "3":
        number = db_manager.get_avg_salary()
        number1 = number[0][0]
        print(round(number1, 2))
    elif index == "4":
        keyword = input("""Введите слово для поиска вакансий
                            """)
        all_vacancies2 = db_manager.get_vacancies_with_keyword(keyword)
        if all_vacancies2:
            print(f"Вакансии, содержащие ключевое слово '{keyword}':")
            for vacancy in all_vacancies2:
                print(vacancy)
        else:
            print(f"Вакансии с ключевым словом '{keyword}' не найдены.")
    elif index == "5":
        pprint.pprint(db_manager.get_companies_and_vacancies_count())
    else:
        print("Введите еще раз корректный запрос")
