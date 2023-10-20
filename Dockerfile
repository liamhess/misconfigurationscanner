FROM python:3.8.18-alpine3.17

COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]
