FROM python:3.9-slim

WORKDIR /tmp

COPY . .

RUN ls -la

RUN \
    # there's no need to run this, since all of these packages are already up to date in the image
    # python -m pip install --upgrade pip setuptools wheel &&\
    python -m pip install .

RUN env

ENTRYPOINT [ "python", "-m", "pyactions" ]
