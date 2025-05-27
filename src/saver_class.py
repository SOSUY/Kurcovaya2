import json
import os
from abc import ABC, abstractmethod

from src.hh_class import Vacancy


class DataSaverInterface(ABC):  # pragma: no cover
    """Интерфейс для классов сохранения данных"""

    @abstractmethod
    def __init__(self, data, filename="vacancies"):
        self.data = data
        self.filename = filename

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def store_data(self):
        pass

    @abstractmethod
    def clear_data(self):
        pass

    @abstractmethod
    def append_vacancy(self, vacancy):
        pass


class JsonFileSaver(DataSaverInterface):
    """Класс для сохранения данных в JSON-файл, позволяет считывать, очищать и добавлять отдельные вакансии"""

    def __init__(self, data: dict, filename: str = "vacancies"):
        self.data = data
        self.filename = filename

    def load_data(self) -> dict:
        """Читает данные из JSON-файла"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "..", "data")
        file_path = os.path.join(data_dir, f"{self.filename}.json")
        with open(file_path, encoding="utf-8") as file:
            return json.load(file)

    def store_data(self):
        """Сохраняет новые вакансии в JSON-файл без повторений и перезаписи существующих данных"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "..", "data")
        file_path = os.path.join(data_dir, f"{self.filename}.json")

        existing_data = {}
        if os.path.exists(file_path):
            try:
                existing_data = self.load_data()
                if not isinstance(existing_data, dict) or 'items' not in existing_data:
                    existing_data = {"items": []}
            except json.JSONDecodeError:
                existing_data = {"items": []}
        else:
            existing_data = {"items": []}

        existing_vacancies = set((v["name"], v["url"]) for v in existing_data["items"])
        updated_items = []

        for item in self.data["items"]:
            salary_from = item.get("salary", {}).get("from", 0)
            salary_to = item.get("salary", {}).get("to", 0)
            requirement = item["snippet"]["requirement"]
            vacancy_obj = Vacancy(item["name"], item["alternate_url"], salary_from, salary_to, requirement)
            unique_key = (vacancy_obj.name, vacancy_obj.url)

            if unique_key not in existing_vacancies:
                updated_items.append(vacancy_obj.main_data())
                existing_vacancies.add(unique_key)

        existing_data["items"].extend(updated_items)

        with open(file_path, "w", encoding="utf-8") as output_file:
            json.dump(existing_data, output_file, ensure_ascii=False, indent=2)

    def clear_data(self):
        """Очищает весь файл с вакансиями"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "..", "data")
        file_path = os.path.join(data_dir, f"{self.filename}.json")
        with open(file_path, "w", encoding="utf-8") as empty_file:
            json.dump({}, empty_file)

    def append_vacancy(self, vacancy: dict):
        """Добавляет отдельную вакансию в существующий файл"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, "..", "data")
        file_path = os.path.join(data_dir, f"{self.filename}.json")

        if isinstance(vacancy, Vacancy):
            vacancy_dict = vacancy.main_data()
            current_data = self.load_data()
            if not any(v == vacancy_dict for v in current_data["items"]):
                current_data["items"].append(vacancy_dict)
            with open(file_path, "w", encoding="utf-8") as update_file:
                json.dump(current_data, update_file, ensure_ascii=False, indent=2)
        else:
            print("Ошибка! Можно добавить только объект типа Vacancy.")
