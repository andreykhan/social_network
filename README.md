### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/andreykhan/social_network.git
```

```
cd social_network
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

# SNET

### Описание 

pet проект. Работает регистрация, публикация/редактирование постов, подписка на авторов. 

### Алгоритм регистрации пользователей: 

1. Пользователь отправляет запрос с параметром *email* на */auth/email/*. 

2. **YaMDB** отправляет письмо с кодом подтверждения (*confirmation_code*) на адрес *email*. 

3. Пользователь отправляет запрос с параметрами *email* и *confirmation_code* на */auth/token/*, в ответе на запрос ему приходит *token* (JWT-токен). 

4. При желании пользователь отправляет PATCH-запрос на */users/me/* и заполняет поля в своём профайле (описание полей — в документации). 

Подробная API документация находится по адресу /redoc 

### Установка 

Проект собран в Docker 20.10.06 и содержит три образа: 

- web - образ проекта 

- postgres - образ базы данных PostgreSQL v 12.04 

- nginx - образ web сервера nginx 

#### Команда клонирования репозитория: 

```bash 

git clone https://github.com/PavelKhanOff/infra_sp2 

``` 

#### Запуск проекта: 

- [Установите Докер](https://docs.docker.com/engine/install/) 

- Выполнить команду:  

```bash 

docker pull pavelkhan/api_yamdb_web:v1.16.06.2021 

``` 

#### Первоначальная настройка Django: 

```bash 

- docker-compose exec web python manage.py migrate --noinput 

- docker-compose exec web python manage.py collectstatic --no-input 

``` 

#### Загрузка тестовой фикстуры в базу: 

```bash 

docker-compose exec web python manage.py loaddata fixtures.json 

``` 

#### Создание суперпользователя: 

```bash 

- docker-compose exec web python manage.py createsuperuser 

``` 

#### Заполнение .env: 

Чтобы добавить переменную в .env необходимо открыть файл .env в корневой директории проекта и поместить туда переменную в формате имя_переменной=значение. 

Пример .env файла: 

 

DB_ENGINE=my_db 