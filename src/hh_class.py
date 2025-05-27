from abc import ABC, abstractmethod
from typing import Any
import requests


class BaseAPIService(ABC):  # pragma: no cover
    """Абстрактный базовый класс для сервисов API"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def check_connection(self):
        pass

    @abstractmethod
    def retrieve_vacancies(self, search_query: str, max_results: int = 100):
        pass


class HeadHunterService(BaseAPIService):
    """Сервис для работы с API HeadHunter, получает данные о вакансиях в формате JSON"""

    def __init__(self):
        self.api_endpoint = "https://api.hh.ru/vacancies"

    def _check_connection(self) -> bool:
        """Проверяет подключение к API, отправляя тестовый запрос"""
        response = requests.get(self.api_endpoint)
        return response.status_code == 200

    def retrieve_vacancies(self, search_query: str, max_results: int = 100) -> Any:
        """Загружает вакансии по заданному запросу и ограничению количества записей"""
        if hasattr(self, "_check_connection") and callable(getattr(self, "_check_connection")):
            if getattr(self, "_check_connection")():
                parameters = {
                    "text": search_query,
                    "per_page": max_results,
                    "search_field": "name",
                }
                response = requests.get(url=self.api_endpoint, params=parameters)
                return response.json()
            else:
                error_status = requests.get(
                    url=self.api_endpoint,
                    params={
                        "text": search_query,
                        "per_page": max_results,
                        "search_field": "name",
                    },
                ).status_code
                print(f"Произошла ошибка подключения: {error_status}")
                return None
