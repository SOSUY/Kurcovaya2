from typing import Union


def select_jobs(jobs_list: dict, keywords: list) -> Union[list, dict]:
    """
    Фильтрует вакансии по указанным ключевым словам в требованиях и возвращает отфильтрованный список вакансий
    """
    filtered_jobs = []

    # Если список ключевых слов пуст, возвращаем исходный список вакансий
    if not keywords:
        return jobs_list["items"]

    # Проходим по каждой вакансии в списке
    for job in jobs_list["items"]:
        try:
            # Проверяем наличие хотя бы одного ключевого слова в требованиях вакансии
            if any(keyword.lower() in job["snippet"]["requirement"].lower() for keyword in keywords):
                filtered_jobs.append(job)
        except Exception:
            # Пропускаем вакансию, если возникла ошибка при обработке
            continue

    return filtered_jobs

