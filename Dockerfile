FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /home 

COPY ./requirements.txt /home/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /home/requirements.txt

COPY . /home

CMD ["gunicorn", "--conf", "app/gunicorn_conf.py", "--bind", "0.0.0.0:80", "main:app"]
