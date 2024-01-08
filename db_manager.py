import psycopg2

class DBManager():
    """Класс для взаимодействия с базой данных"""


    def get_companies_and_vacancies_count(self, cur):
        """Метод получает список всех кампаний и количество вакансий у каждой кампании"""
        cur.execute(f"""Select employer, COUNT(vacancy_name) from employers  as vacancy_count
            join vacancies using employer_id order by vacancies_count DESC""")
        result = cur.fetchall()
        return result
    def get_all_vacancies(self, cur):
        """Получает список всех вакансий"""
        cur.execute(f"""Select * from vacancies order by salary_min DESC""")
        result = cur.fetchall()
        return result


    def get_avg_salary(self, cur):
        """Получает среднюю зарплату по вакансиям"""
        cur.execute(f"""Select AVG(salary_min) from vacancies""")
        result = cur.fetchall()
        return result

    def get_vacancies_with_higher_salary(self, cur):
        """Получает список всех вакансий у которых з/п выше средней"""
        cur.execute(f"""Select * from vacancies where salary_min > AVG(salary_min)
            order by salary_min DESC""")
        result = cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword, cur):
        """Получает вакансии по ключевому слову"""
        cur.execute(f"""Select * from vacancies where vacancy_name like %{keyword}%""")
        result = cur.fetchall()
        return result