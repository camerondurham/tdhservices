FROM python:latest

WORKDIR /app

COPY ./tdhwebscraper /app

RUN pip3.7 install -r requirements.txt

EXPOSE 4000

CMD ["python", "api.py"]
