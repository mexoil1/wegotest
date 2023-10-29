FROM python:3.12

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir

COPY wegotrip/. .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wegotrip.wsgi"]