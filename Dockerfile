FROM python:3.9-slim-bullseye

WORKDIR /app
ADD . /app/

RUN apt-get update
RUN apt-get install build-essential -y --no-install-recommends

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#RUN python3 -m pip install -r requirements_dev.txt
#RUN python3 -m pip install -r requirements.txt
#RUN python3 setup.py develop
RUN make install

#RUN python3 src/main.py --find-best true