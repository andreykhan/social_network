FROM python:3.7-slim

# Запустить команду создания директории внутри контейнера
RUN mkdir /app

# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY requirements.txt /app

# Выполнить установку зависимостей внутри контейнера.
RUN pip install -r /app/requirements.txt --no-cache-dir

# Скопировать содержимое директории /social_network c локального компьютера
# в директорию /app.
COPY . /app

# Сделать директорию /app рабочей директорией. 
WORKDIR /app

# Выполнить запуск сервера разработки при старте контейнера.
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ] 