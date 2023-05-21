FROM registry.access.redhat.com/ubi8

RUN yum install python3 vim git sudo -y && \
    useradd keys4 && \
    echo "keys4:keys4" | chpasswd && \
    usermod -aG wheel keys4

USER keys4

WORKDIR /home/keys4

COPY ./code/ .

RUN pip3 install --user -r app/requirements.txt

CMD python3 runner.py
