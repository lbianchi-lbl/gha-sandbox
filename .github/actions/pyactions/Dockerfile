FROM python:3.9-slim

RUN \
    # there's no need to run this, since all of these packages are already up to date in the image
    # python -m pip install --upgrade pip setuptools wheel &&\
    python -m pip install ghapi pydantic

COPY ./pyactions pyactions

RUN env

ENTRYPOINT [ "python", "-m", "pyactions" ]
