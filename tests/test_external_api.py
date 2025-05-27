from unittest.mock import Mock, patch

from src.external_api import API_HH


@patch("src.external_api.requests.get")
def test_get_vacancies_code200(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"name": "Python Developer"}]}
    mock_get.return_value = mock_response

    test_api = API_HH()
    assert test_api._BaseAPI__connect() == True
    result = test_api.get_vacancies("Python", top_N=1)

    mock_get.assert_called_with(
        url="https://api.hh.ru/vacancies", params={"text": "Python", "per_page": 1, "search_field": "name"}
    )
    assert result == {"items": [{"name": "Python Developer"}]}


@patch("src.external_api.requests.get")
def test_get_vacancies_code403(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.json.return_value = None
    mock_get.return_value = mock_response

    test_api = API_HH()
    test_api.get_vacancies("Python", top_N=1)

    mock_get.assert_called_with(
        "https://api.hh.ru/vacancies", params={"text": "Python", "per_page": 1, "search_field": "name"}
    )
    captured = capsys.readouterr()
    assert captured.out == "Сервер не доступен ошибка: 403\n"
