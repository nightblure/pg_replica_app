# pg_replica_app

1. В директории клона репозитория развернуть контейнеры с БД: docker-compose up -d

2. Выполнить команды в docker-терминале мастер-контейнера:

2.1. Поправить конфигурацию мастера (включить репликацию):
psql -U postgres -c "ALTER SYSTEM SET wal_level = logical"
psql -U postgres -c "ALTER SYSTEM SET listen_addresses = '*'"

2.2. Ребутнуть мастер-контейнер

2.3. Создать публикацию
psql -U postgres --echo-all -c "select * from pg_settings where name = 'wal_level'"
psql -U postgres -d master_db -c "CREATE PUBLICATION publication FOR TABLE app__item"


3. Установка зависимостей в локальное виртуальное окружение:
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt


4. Запуск:
cd root
python manage.py runserver

* Миграции нужны, если в процессе развертывания docker-compose не был развернут дамп для мастера и реплики. В нашем случае дамп есть, но на всякий случай пусть останутся команды для миграций
python manage.py migrate --database=default
python manage.py migrate --database=replica
