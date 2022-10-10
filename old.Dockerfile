FROM docker.javra.com/python-fast-api:v1

WORKDIR /usr/src/api

COPY . /usr/src/api/

#RUN pip install -r /usr/src/api/requirements.txt

EXPOSE 3334
