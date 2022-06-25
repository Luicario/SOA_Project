FROM python:3.10.5-alpine3.16
RUN pip install celery redis
COPY . .
CMD ["celery","-A","calculator","worker","--pool=solo","-l","info"]