FROM python:3.10

RUN apt update
RUN apt install wget

WORKDIR /app

RUN wget -O /app/mc https://dl.min.io/client/mc/release/linux-amd64/mc
RUN chmod +x mc

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./backend /app/backend
COPY ./migration /app/migration
COPY ./alembic.ini /app/alembic.ini

COPY backend/prestart.sh /app/prestart.sh
RUN chmod +x /app/prestart.sh

COPY backend/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]