FROM python:slim

WORKDIR /app

COPY ./app /app

RUN pip3.7 install -r requirements.txt

EXPOSE 3000

CMD ["python", "api.py"]
