import psycopg2

class DBManager():
    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self, keyword, cur):
        cur.execute(f"""Select * from vacancies where vacancy_name like %{keyword}%""")
        result = cur.fetchall()
        return result