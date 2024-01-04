import psycopg2

class DBManager():
    def get_companies_and_vacancies_count(self, cur):
        pass
    def get_all_vacancies(self):
        cur.execute(f"""Select employer, vacancy_name, salary_min, vacancy_url 
        from vacancies order by salary_min DESC""")
        result = cur.fetchall()
        return result


    def get_avg_salary(self):
        cur.execute(f"""Select AVG(salary_min) from vacancies""")
        result = cur.fetchall()
        return result

    def get_vacancies_with_higher_salary(self):
        cur.execute(f"""Select employer, vacancy_name, salary_min, vacancy_url
            from vacancies where salary_min > AVG(salary_min)
            order by salary_min DESC""")
        result = cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword, cur):
        cur.execute(f"""Select * from vacancies where vacancy_name like %{keyword}%""")
        result = cur.fetchall()
        return result