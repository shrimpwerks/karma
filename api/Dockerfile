FROM python:3.8-slim
WORKDIR /app

COPY . ./
RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:80", "api:app", "--reload"]
