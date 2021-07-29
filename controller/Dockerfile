FROM python:3-slim-buster

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip3 install watchdog[watchmedo] pipenv
COPY Pipfile .
RUN pipenv install

COPY . .

CMD [ "pipenv", "run", "python ", "./app.py" ]
