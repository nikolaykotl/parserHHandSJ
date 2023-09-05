Программа Парсер вакансий.
Это программа для поиска вакансий на hh.ru и superjob.ru. Программа позволяет 
пользователю выбрать платформу для поиска вакансий, ввести поисковый запрос, 
фильтровать вакансии, сортировать по зарплате, выводить топ-n вакансий по зарплате.

1.Склонируйте репозиторий на свой локальный компьютер

2.Для поиска вакансий на платформе superjob.ru необходимо зарегистрировать приложение
(https://api.superjob.ru/?from_refresh=1)
и получить секретный ключ X-Api-App-Id. После того как получите секретный ключ, создайте
файл .env и запишите данные в формате 'X_Api_App_Id' = 'секретный ключ'
Authorization = Bearer r.000000010000001.example.access_token

3.Установите зависимости: pip install -r requirements.txt

Запустите программу
python3 main.py

При запуске программы вам будет предложено выбрать платформу для поиска вакансий (HeadHunter, SuperJob или оба) или завершить программу.
Выберите соответствующую цифру и нажмите Enter.
Введите поисковый запрос.
Введите количество вакансий, которые хотите получить.
Программа выведет список найденных вакансий.
Вам будет предложено отфильтровать вакансии.
После фильтрации (или без нее) вы можете отсортировать вакансии по зарплате.
Программа выведет отсортированный список вакансий.
После сортировки (или без нее) вы можете получить топ-n вакансий по зарплате.
Далее будет предложено удалить найденные вакансии (при выборе 1 - найденные вакансии из файла удаляются).

Зависимости:
certifi==2023.7.22
charset-normalizer==3.2.0
idna==3.4
python-dotenv==1.0.0
requests==2.31.0
urllib3==2.0.4
