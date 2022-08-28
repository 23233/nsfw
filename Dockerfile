FROM python:3.9-alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]