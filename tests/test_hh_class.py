from src.hh_class import Vacancy

vacancy_1 = Vacancy(
    "Python Developer", "<https://hh.ru/vacancy/123456>", 100000, 150000, "Требования: опыт работы от 3 лет..."
)
vacancy_2 = Vacancy(
    "Java Developer", "<https://hh.ru/vacancy/1789>", 120000, 180000, "Требования: опыт работы от 4 лет..."
)


def test_vacancy_init_print(capsys):
    assert vacancy_1.name == "Python Developer"
    print(vacancy_1)
    captured = capsys.readouterr()
    assert captured.out == (
        "    "
        "=========================================================================\n"
        "    Название: Python Developer\n"
        "    Ссылка: <https://hh.ru/vacancy/123456>\n"
        "    Зарплата от 100000 до 150000\n"
        "    Описание: Требования: опыт работы от 3 лет...\n"
        "    "
        "=========================================================================\n"
    )


def test_vacancies_compare():
    assert (vacancy_1 > vacancy_2) == False
    assert (vacancy_1 < vacancy_2) == True
    assert (vacancy_1 >= vacancy_2) == False
    assert (vacancy_1 <= vacancy_2) == True
    assert (vacancy_1 == vacancy_2) == False
    assert (vacancy_1 != vacancy_2) == True


def test_validate_vacancy():
    broken_vacancy = Vacancy("name", "<https://hh.ru/vacancy/1>", "some_salary", ["10"], "some_desc")
    assert broken_vacancy.salary_from == 0
    assert broken_vacancy.salary_to == 0


def test_main_data_vacancy():
    assert vacancy_1.main_data() == {
        "name": "Python Developer",
        "alternate_url": "<https://hh.ru/vacancy/123456>",
        "salary_from": 100000,
        "salary_to": 150000,
        "snippet": {"requirement": "Требования: опыт работы от 3 лет..."},
    }
