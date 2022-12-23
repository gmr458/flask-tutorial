FROM python:3.11.1-alpine3.17

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . .

CMD [ "flask", "--app", "flaskr", "--debug", "run", "--host", "0.0.0.0" ]
