FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 80
EXPOSE 8080
EXPOSE 8000
COPY . .

CMD [ "pytest", "main.py"]
