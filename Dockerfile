FROM python:3.7-slim

ADD . /

RUN pip install -r requirements.txt

WORKDIR /home/aditya/

EXPOSE 3141

CMD [ "python", "backend/app.py" ]