
ARG BASE_PRIVATE_REGISTRY=""
FROM ${BASE_PRIVATE_REGISTRY}python:3.7.4-slim
LABEL maintainer="yehiyam@gmail.com"
RUN mkdir -p /hkube/algorithm-example-python
WORKDIR /hkube/algorithm-example-python/
COPY ./requirements.txt /hkube/algorithm-example-python/requirements.txt
RUN pip install -r requirements.txt
COPY . /hkube/algorithm-example-python
CMD ["python3","-u", "app.py"]