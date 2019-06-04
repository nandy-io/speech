FROM resin/rpi-raspbian

RUN apt-get update && apt-get install -y python-pip rpi-update && \
    SKIP_WARNING=1 rpi-update && \
    apt-get install -y omxplayer && \
    mkdir -p /opt/nandy-io

WORKDIR /opt/nandy-io

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD bin bin
ADD lib lib
ADD test test

ENV PYTHONPATH "/opt/nandy-io/lib:${PYTHONPATH}"

CMD "/opt/nandy-io/bin/daemon.py"
