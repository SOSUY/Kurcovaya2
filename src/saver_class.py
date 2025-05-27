import json
import os
from abc import ABC, abstractmethod

from src.hh_class import Vacancy


class BaseSave(ABC):  # pragma: no cover
    """Базовый класс для File_Save"""

    @abstractmethod
    def __init__(self, data, name="vacancies"):
        self.data = data
        self.__name = name

    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def read_file(self):
        pass

    @abstractmethod
    def delete_vacancies(self):
        pass

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass


class File_Save(BaseSave):
    """Класс для сохранения данных в файл для дальнейшей работы с ним,
    может также удалять все вакансии в файле, читать его, и добавлять вакансии отдельно"""

    def __init__(self, data:dict, name:str="vacancies"):
        self.data = data
        self.__name = name

    def read_file(self) -> dict:
        """Метод, который читает данные из json файла и выводит его"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "..", "data")
        file_path = os.path.join(data_dir, f"{self.__name}.json")
        with open(file_path, encoding="utf-8") as r:
            file = json.load(r)
        return file

    def save_to_file(self):
        """Метод для сохранения информации в файл json без перезаписывания и дублирования"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "..", "data")
        file_path = os.path.join(data_dir, f"{self.__name}.json")
        if os.path.exists(file_path):
            try:
                old_data = self.read_file()
                if not isinstance(old_data, dict) or 'items' not in old_data:
                    old_data = {"items": []}
            except json.JSONDecodeError:
                old_data = {"items": []}
        else:
            old_data = {"items": []}

        old_vacancies = {(item["name"], item["alternate_url"]) for item in old_data['items']}
        new_data = []
        for i in self.data["items"]:
            salary_from = 0
            salary_to = 0

            if i.get("salary"):
                salary_from = i["salary"].get("from") or 0
                salary_to = i["salary"].get("to") or 0

            vacancy = Vacancy(i["name"], i["alternate_url"], salary_from, salary_to, i["snippet"]["requirement"])
            key = (vacancy.name,vacancy.url)
            if key not in old_vacancies:
                new_data.append(vacancy.main_data())
                old_vacancies.add(key)

        old_data['items'].extend(new_data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(old_data, f, ensure_ascii=False, indent=2)

    def delete_vacancies(self):
        """Метод удаляющий все данные из json файла"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "..", "data")
        file_path = os.path.join(data_dir, f"{self.__name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({}, f)

    def add_vacancy(self, vacancy:dict):
        """Метод добавляющий отделённую вакансию в файл"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "..", "data")
        file_path = os.path.join(data_dir, f"{self.__name}.json")
        if isinstance(vacancy, Vacancy):
            vacancy = vacancy.main_data()
            with open(file_path, encoding="utf-8") as r:
                data = json.load(r)
            if not any(v == vacancy for v in data["items"]):
                data["items"].append(vacancy)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            print("Можно добавлять только main_data из класса Vacancy")
