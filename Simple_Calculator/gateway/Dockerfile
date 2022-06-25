FROM python:3.10.5-alpine3.16
RUN pip install celery redis Werkzeug nameko
COPY . .
CMD ["python", "main.py", "run"]