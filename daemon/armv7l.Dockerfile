FROM klotio/rpi-raspbian:0.1

RUN apt-get update && apt-get install -y alsa-utils mpg123 && \
    mkdir -p /opt/nandy-io

WORKDIR /opt/nandy-io

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD bin bin
ADD lib lib
ADD test test

ENV PYTHONPATH "/opt/nandy-io/lib:${PYTHONPATH}"

CMD "/opt/nandy-io/bin/daemon.py"
