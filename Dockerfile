FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN useradd -ms /bin/bash admin
EXPOSE 80
EXPOSE 8080
EXPOSE 8000
COPY . .
RUN chown -R admin:admin /app
RUN chmod 777 /app
USER admin
CMD [ "pytest", "main.py"]
