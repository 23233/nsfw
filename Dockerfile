FROM python:3.8-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]