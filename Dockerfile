FROM python:3.6

ADD ./src /src
ADD ./policies /policies
ADD ./entrypoint.sh /entrypoint.sh
ADD ./policy-diff.sh /policy-diff.sh
ADD ./requirements.pip /requirements.pip
CMD /entrypoint.sh
RUN pip install -r requirements.pip
