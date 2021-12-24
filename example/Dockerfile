FROM debian:bullseye

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip
    
RUN pip3 install Django==4.0 \
                 uwsgi==2.0.20 \
                 django-compressor==3.1

COPY resources/uwsgi.ini /etc/

ADD app/ /opt/example/

RUN pip3 install --no-deps django-infinite-scroll

RUN cd /opt/example/ && \
    python3 manage.py collectstatic --no-input && \
    chown www-data.www-data -R /opt/example

WORKDIR /opt/example

ENTRYPOINT ["uwsgi", "--ini", "/etc/uwsgi.ini"]
