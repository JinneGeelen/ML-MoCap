FROM balenalib/raspberry-pi-python:3.7-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

CMD ["python3", "app.py"]
