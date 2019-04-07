FROM python:3.7-slim

COPY . /

RUN pip install -r requirements.txt

EXPOSE 3141
EXPOSE 27017

CMD [ "python", "app.py" ]