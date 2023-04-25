FROM python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /usr/src

COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]