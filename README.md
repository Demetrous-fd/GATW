# Тестовое задание от _"Гринатом"_
## Требования
Реализовать веб-сервис, который принимает изображения jpeg в количестве от 1 до 15
и сохраняет их в S3 хранилище Minio, дата и название сохраненных изображений помещаются
в БД Postgres в таблицу _inbox_.

### Зависимости

* Python 3.10

* Docker и Docker-compose

### Запуск через docker-compose

1. С клонируйте репозиторий:
   - `git clone https://github.com/demetrous-fd/Grasscutter.git`
2. Перейдите в папку репозитория
3. Создайте _.env_ по образцу _.env.example_ и установите свои переменные окружения (`не используйте @ в переменных для postgres`) 
4. Для запуска проекта выполните:
   - `sudo docker-compose up -d`

### Запуск тестов
- В папке репозитория выполните:
  - `sudo docker-compose exec api pytest backend/tests/frames_endpoint.py`