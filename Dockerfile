FROM python:3.8-slim-bullseye
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN pip3 uninstall opencv-python && pip3 install opencv-python-headless -i https://mirrors.aliyun.com/pypi/simple/
COPY . /app

EXPOSE 5000
# 可以防止中文乱码问题
ENV LANG C.UTF-8
CMD ["gunicorn", "app:app", "-c", "./gunicorn.conf.py"]