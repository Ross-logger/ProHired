FROM python:3.10

WORKDIR /ProHired

COPY ./requirements.txt /ProHired/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /ProHired/requirements.txt

COPY ./src /ProHired/src

COPY .env /ProHired/.env

CMD ["uvicorn", "src.main:app", "--reload", "--port", "80", "--host", "0.0.0.0"]