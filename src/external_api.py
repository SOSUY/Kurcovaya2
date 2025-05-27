from abc import ABC, abstractmethod
from typing import Any
import requests


class BaseAPI(ABC):  # pragma: no cover
    """Базовый класс для API_HH"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __connect(self):
        pass

    @abstractmethod
    def get_vacancies(self, desc, top_N=100):
        pass


class API_HH(BaseAPI):
    """Класс для работы с HeadHunterAPI, загружает вакансии из hh.ru json файлом"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"

    def _BaseAPI__connect(self) -> bool:
        """Делает базовый запрос API и проверяет статус код"""
        return True if requests.get(self.__url).status_code == 200 else False

    def get_vacancies(self, desc:str, top_N:int = 100) -> Any:
        """Возвращает вакансии по поиску и сколько первых вакансий показать"""
        if self._BaseAPI__connect:
            if self._BaseAPI__connect():
                params = {"text": desc, "per_page": top_N, "search_field": "name"}
                vacancies = requests.get(url=self.__url, params=params)
                return vacancies.json()
            else:
                print(
                    f'Сервер не доступен ошибка: {requests.get(self.__url, params={"text": desc, "per_page": top_N, "search_field": "name"}).status_code}'
                )
                return None
