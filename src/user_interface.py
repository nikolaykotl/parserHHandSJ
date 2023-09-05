from src.vacancy_api import HeadHunterAPI, SuperJobAPI
from src.vacancy_manager import JSONSaver
import sys

def user_interaction():
    """
    Функция взаимодействия с пользователем по поиску вакансий, их фильтрации и сортировке.
    """
    print("Программа поиска вакансий на платформах hh.ru и superjob.ru\n")
          # Выбор платформы
    platforms = {
        1: "HeadHunter",
        2: "SuperJob",
        3: "На всех платформах",
        4: "Завершить программу"
    }
    user_choice = int(input("Выберите пожалуйста платформу для поиска (указав цифру): \n1: HeadHunter,\n2: SuperJob,\n3: На всех платформах,\n4: Завершить программу\n"))
    if user_choice == 4:
        print('Программа завершена')
        sys.exit()
    elif user_choice == 1 or user_choice == 2 or user_choice == 3:
        print(f"Для поиска выбрана платформа '{platforms[user_choice]}'\n")
    else:
        raise print(f"Ошибка! Неверно указана платформа.")


    vacancies = []
    query = input("Введите поисковый запрос: ")
    num_vc_query = int(input("Введите количество вакансий в запросе: "))

    hh = HeadHunterAPI(query)
    superjob = SuperJobAPI(query)

    if user_choice == 1:
        hh.get_vacancies(num_vc_query)
        vacancies.extend(hh.get_formatted_vacancies())
    elif user_choice == 2:
        superjob.get_vacancies(num_vc_query)
        vacancies.extend(superjob.get_formatted_vacancies())
    elif user_choice == 3:
        hh.get_vacancies(num_vc_query // 2)
        superjob.get_vacancies(num_vc_query - len(hh.vacancies))
        vacancies.extend(hh.get_formatted_vacancies())
        vacancies.extend(superjob.get_formatted_vacancies())

    json_saver = JSONSaver()
    for vc in vacancies:
       json_saver.add_vacancy(vc)

    vacancies = json_saver.get_vacancies()
    for vacancy in vacancies:
        print(f"\n{vacancy}")
    user_choice_filter = int(input("Желаете отфильтровать вакансии?(1: Да, 2: Нет) "))


    if user_choice_filter == 1:
        filter_words = input("Введите ключевые слова для фильтрации вакансий (названию, опыту, зарплате, городу): ").split()
        vacancies = json_saver.filter_vacancies(filter_words)

        if len(vacancies) == 0:
            print("Нет вакансий, соответствующих заданным критериям.")
            user_choice_vac = int(input("Желаете удалить вакансии: 1: Да, 2: Нет "))
            if user_choice_vac == 1:
                json_saver.delete_vacancy(vacancies)
                print("Вакансии удалены.")
            return
        else:
            print("\nОтфильтрованные вакансии:\n")
            for vc in vacancies:
                print(vc)


    # Сортировка

    user_choice_sorted = int(input("Желаете отсортировать вакансии по зарплате?(1: Да, 2: Нет) "))

    if user_choice_sorted == 1:
        print("Сортировка будет производиться по убыванию.")
        vacancies = json_saver.sort_vacancies_by_salary()

        print("\nОтсортированные вакансии:\n")
        for vc in vacancies:
            print(vc)

    user_top = int(input("Желаете вывести ТОП вакансии по зарплате?(1: Да, 2: Нет) "))

    if user_top == 1:
        user_top_n = int(input("Укажите количество вакансий в ТОПе: "))
        vacancies_top = json_saver.salary_top(user_top_n)

        print(f"ТОП-{user_top_n} вакансии по зарплате:\n")
        for vc_top in vacancies_top:
            print(vc_top)

    user_choice_del = int(input("Желаете удалить вакансии?(1: Да, 2: Нет) "))
    if user_choice_del == 1:
        json_saver.delete_vacancy(vacancies)
        print("Вакансии удалены.")
    else:
        print("Вакансии сохранены в файле vacancies.json")

    print("Программа завершена.")