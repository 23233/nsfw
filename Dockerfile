FROM python:3.8-alpine
WORKDIR /app
COPY ./requirements.txt .
COPY ./onnxruntime-1.12.1-cp38-cp38-manylinux_2_27_x86_64.whl .
RUN pip3 install ./onnxruntime-1.12.1-cp38-cp38-manylinux_2_27_x86_64.whl
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . /app

EXPOSE 5000

CMD ["gunicorn", "start:app", "-c", "./gunicorn.conf.py"]