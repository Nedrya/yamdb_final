# Создать образ на основе базового слоя python (там будет ОС и интерпретатор Python).
# 3.7 — используемая версия Python.
# slim — обозначение того, что образ имеет только необходимые компоненты для запуска,
# он не будет занимать много места при развёртывании.
FROM python:3.7-slim
# Создать директорию вашего приложения.
RUN mkdir /app
# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY ./requirements.txt /app

# Копируем ENV.
ENV DB_ENGINE=django.db.backends.postgresql 
ENV DB_NAME=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV DB_HOST=db
ENV DB_PORT=5432
# Выполнить установку зависимостей внутри контейнера.
RUN pip3 install -r app/requirements.txt --no-cache-dir

# Скопировать содержимое директории /api_yamdb c локального компьютера
# в директорию /app.

COPY ../api_yamdb/ /app
WORKDIR  /app
# Выполнить запуск сервера разработки при старте контейнера.
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ] 