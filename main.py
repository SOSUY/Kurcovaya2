from src.external_api import HeadHunterService
from src.filter import select_jobs
from src.hh_class import Vacancy
from src.saver_class import JsonFileSaver


def main():
    """Основная программа, где происходят почти все действия с классами и функциями"""
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()

    api = HeadHunterService()
    vacancies = api.retrieve_vacancies(search_query, top_n)
    saver = JsonFileSaver(vacancies)
    saver.store_data()
    vacancies["items"] = select_jobs(vacancies, filter_words)

    for i in vacancies["items"]:
        salary_from = 0
        salary_to = 0
        if i.get("salary"):
            salary_from = i["salary"].get("from") or 0
            salary_to = i["salary"].get("to") or 0

        vacancy = Vacancy(i["name"], i["alternate_url"], salary_from, salary_to, i["snippet"]["requirement"])
        print(vacancy)


main()
