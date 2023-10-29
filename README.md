# Тестовое задание
## Стек:
1. `Python`
2. `Django`
3. `PostgreSQL`
4. `Docker`
## Как запустить
1. В директории с `docker-compsoe.yml` файлами создайте файл `.env` в котором впишите ваши настройки (готовый `.env` файл есть в письме)
2. Запустите проект командой `docker compose up -d`
3. Выполните миграции `docker compose exec backend python manage.py migrate`
4. Создайте админа `docker compose exec backend python manage.py createsuperuser`
5. Загрузите статику и скопируйте `docker compose exec backend python manage.py collectstatic` и `docker compose exec backend cp -r /app/collect_static/. /static_backend/static_backend/`
По адресу `http://127.0.0.1/swagger/` у вас будет документация
По адресу `http://127.0.0.1/admin/` у вас будет админ панель джанги
Командой `docker compose exec backend python manage.py test` вы можете запустить тесты