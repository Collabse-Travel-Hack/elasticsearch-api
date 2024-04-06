FROM python:3.11-alpine
 
WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./src /code/src

EXPOSE 80

# ENV PYTHONPATH="${PYTHONPATH}:./src"

ENV ELASTICSEARCH_HOST=http://158.160.14.223
ENV ELASTICSEARCH_PORT=9200

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]