
ARG BASE_PRIVATE_REGISTRY=""
FROM ${BASE_PRIVATE_REGISTRY}python:3.7.4
LABEL maintainer="yehiyam@gmail.com"
ADD ./requirements.txt /hkube/algorithm-example-python/requirements.txt
WORKDIR /hkube/algorithm-example-python/
RUN pip install -r requirements.txt
RUN mkdir -p /hkube-logs
COPY . /hkube/algorithm-example-python
CMD ["/bin/sh", "-c", "python -u app.py 2>&1 |tee /hkube-logs/stdout.log"]
