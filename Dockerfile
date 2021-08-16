FROM python:3.9.5

ENV PYTHONUNBUFFERED 1

EXPOSE 8080

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0" ,"--port", "8080"]
