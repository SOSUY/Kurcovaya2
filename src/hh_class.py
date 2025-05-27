class Vacancy:
    """Класс для создания вакансий и работы с ними,
    их можно сравнивать друг с другом, выводить в консоль,
    а также все зарплаты валидируются в специальном приватном методе"""

    __slots__ = ("__name", "url", "salary_from", "salary_to", "desc")

    def __init__(self, name:str, url:str, salary_from:int, salary_to:int, desc:str):
        self.__name = name
        self.url = url
        self.salary_from = self._validate_salary(salary_from)
        self.salary_to = self._validate_salary(salary_to)
        self.desc = desc

    @property
    def name(self) -> str:
        return self.__name

    def _validate_salary(self, value:int) -> int:
        """Приватный валидатор суммы денег"""
        if isinstance(value, (int, float)) and value > 0:
            return value
        return 0

    def main_data(self) -> dict:
        """Возвращает всю информацию о вакансии как в json файле для работы с ним"""
        return {
            "name": self.__name,
            "alternate_url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "snippet": {"requirement": self.desc},
        }

    def __str__(self) -> str:
        """При вызове print или str для класса будет выводиться вся информация в красивом виде"""
        return f"""    =========================================================================
    Название: {self.__name}
    Ссылка: {self.url}
    Зарплата от {self.salary_from} до {self.salary_to}
    Описание: {self.desc}
    ========================================================================="""

    # Магические методы сравнения
    def __eq__(self, other):
        """Сравнение если два объекта класса равны"""
        return self.salary_from == other.salary_from

    def __ne__(self, other):
        """Сравнение если два объекта класса не равны"""
        return self.salary_from != other.salary_from

    def __lt__(self, other):
        """Сравнение если 2 объекта больше 1 объекта"""
        return self.salary_from < other.salary_from

    def __gt__(self, other):
        """Сравнение если 1 объекта больше 2 объекта"""
        return self.salary_from > other.salary_from

    def __le__(self, other):
        """Сравнение если 2 объекта больше или равен 1 объекту"""
        return self.salary_from <= other.salary_from

    def __ge__(self, other):
        """Сравнение если 1 объекта больше или равен 2 объекта"""
        return self.salary_from >= other.salary_from
