FROM balenalib/raspberry-pi-python:3.7-buster

WORKDIR /app

ENV READTHEDOCS=True

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN apt update && apt install -y gpac --fix-missing

COPY . /app

CMD ["python3", "app.py"]
