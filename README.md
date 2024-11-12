## Краткое Описание

Greenatom backend - это API для системы учета отходов атом эко.
С помощью него можно утилизировать отходы организациям в различные ближайшие хранилища. В данном проекте реализована авторизация пользоваталей через djoser и TokenAuthentication.
Также в этом проекте реализована админка, с помощью которой можно выдавать пользователям права на управление учетом отходов для организаций. Логин и пароль для админки(Login: Danil, password: qwerty12345)

## Инструкция по запуску проекта

1. Клонируйте репозиторий, создайте и активируйте вирутальное окружение

```
git clone git@github.com:Dan1lChirkov/greenatom_backend_test.git
python -m venv venv
source venv/Scripts/activate
```

2. Перейдите в папку waste_managment и установите в вируальное окружение зависимости из файла requirements.txt

```
cd waste_managment/
pip install -r requirements.txt
```

4. В корневой директории проекта создайте файл .env и заполните следующие поля:

```
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...
DB_HOST=...
DB_PORT=5432
SECRET_KEY =...
```

5. Создайте и примените миграции:

```
python manage.py makemigrations
python manage.py migrate
```

6. Запустите локальный сервер разработки.

```
python manage.py runserver
```

## Запуск проекта через docker-compose

1. Запустите контейнеры:

```
docker compose up
```

2. Выполните миграции, соберите статику и загрузите материалы.

```
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic --noinput
docker compose exec backend python manage.py load_csv --path data/capacities.csv --model_name Capacity --app_name core
```

3. Можно создать суперпользователя следующей командой:

```
docker compose exec backend python manage.py createsuperuser
```

4. API будет работать по адресу: http://localhost:8000

5. Чтобы прекратить работу проекта из контейнера, нужно в терминале для запуска контейнеров нажать Ctrl + C