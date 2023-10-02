# Docker-команда FROM указывает базовый образ контейнера
# Наш базовый образ - это Linux с предустановленным python-3.10
FROM python:3.11.5-slim

# Установим переменную окружения
ENV APP_HOME /app

# Установим рабочую директорию внутри контейнера
WORKDIR $APP_HOME

# Встановимо залежності всередині контейнера
COPY pyproject.toml $APP_HOME/pyproject.toml
COPY poetry.lock $APP_HOME/poetry.lock

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only main

# Скопируем остальные файлы в рабочую директорию контейнера
COPY . .

# Запустим наше приложение внутри контейнера
CMD ["python", "Personal_assistant/main.py"]