FROM ubuntu:14.04

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-dev python3-pip
RUN apt-get install -y libcurl4-openssl-dev
RUN apt-get install -y libpq-dev

RUN pip3 install virtualenv
RUN virtualenv -p python3 /venv

ADD . /fermenter
WORKDIR /fermenter
RUN /venv/bin/pip install -r ./requirements.txt

ENTRYPOINT ["./launch.sh"]


