FROM python:3-alpine

WORKDIR /app

ADD app.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "app.py"]
