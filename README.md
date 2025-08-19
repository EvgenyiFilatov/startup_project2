# Проект Администрирования стартапов

Описание проекта
- Веб‑приложение на Django для управления стартапами
- Функциональность: создание, редактирование, просмотр, удаление стартапов и управление участниками
- Аутентификация с помощью Google OAuth2
- Роли участников реализованы через модель StartupDeveloper с полем role
- Реализовано разграничение прав доступа

## Стек технолгий
- Python
- Django
- База данных SQLite
- Google OAuth2
- Дополнительно: dotenv для конфигурации из .env

### Как запустить проект локально
- Склонировать репозиторий
  - git clone https://github.com/EvgenyiFilatov/startup_project2.git
  - cd startup_project2
- Создать виртуальное окружение и активировать
  - python -m venv venv
  - source venv/bin/activate  (Windows: venv\Scripts\activate)
- Установить зависимости
  - pip install -r requirements.txt
- Настроить переменные окружения
  - Скопировать .env.example → .env и заполнить основные поля: SECRETKEY, DEBUG, SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
- Применить миграции
  - python manage.py migrate
- Создать суперпользователя
  - python manage.py createsuperuser
- Запустить сервер
  - python manage.py runserver
- Открыть в браузере
  - http://127.0.0.1:8000
