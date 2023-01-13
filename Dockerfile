FROM python:3.7

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./main.py /code/

CMD ["gunicorn", "main:app", "--preload", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]