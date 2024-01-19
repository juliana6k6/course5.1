import psycopg2

class DBManager():
    """Класс для взаимодействия с базой данных"""

    def __init__(self, user: str='postgres', password: str='1967', host: str ='localhost', port: str ='5432'):
        self.conn = psycopg2.connect(user=user, password=password, host=host, port=port)
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех кампаний и количество вакансий у каждой кампании"""
        self.cursor.execute(f"""Select employers.employer_name, COUNT(*) 
        from employers left join vacancies using (employer_id) group by employers.employer_name""")
        result = self.cursor.fetchall()
        return result



    def get_all_vacancies(self):
        """Получает список всех вакансий"""
        self.cursor.execute(f"""Select * from vacancies order by salary_min DESC""")
        result = self.cursor.fetchall()
        return result


    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        self.cursor.execute(f"""Select AVG(salary_min) as avg_salary from vacancies""")
        result = self.cursor.fetchall()
        return result

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий у которых з/п выше средней"""
        self.cursor.execute(f"""Select * from vacancies where salary_min > (SELECT AVG(salary_min) FROM vacancies)
            order by salary_min DESC""")
        result = self.cursor.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Получает вакансии по ключевому слову"""
        self.cursor.execute(f"Select * from vacancies where vacancy_name like '%{keyword}%' order by salary_min DESC")
        result = self.cursor.fetchall()
        return result

