from typing import Union


def filter_word(data: dict, words: list) -> Union[list, dict]:
    """Фильтрует вакансии по заданным словам в описании и возвращает отфильтрованный список с вакансиями"""
    new_data = []
    if not words:
        return data["items"]
    for i in data["items"]:
        try:
            if any(word.lower() in i["snippet"]["requirement"] for word in words):
                new_data.append(i)
        except Exception:
            continue

    return new_data
