# Устанавливаем базовый образ
FROM python:3.9

# Установка зависимостей
COPY requirements.txt /
RUN apt-get update && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r /requirements.txt

# Копирование кода в контейнер
COPY . /

# Запуск бота
CMD ["python3", "bot.py"]
