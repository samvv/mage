FROM python:3.13
RUN pip install -U pip
RUN pip install pytest
COPY dist/* /dist/
RUN pip install /dist/*
WORKDIR /dist
ENTRYPOINT [ "mage" ]
