FROM python:3.6

ADD ./src /src
ADD ./entrypoint.sh /entrypoint.sh

CMD /entrypoint.sh
