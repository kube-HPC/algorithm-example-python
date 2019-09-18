
ARG BASE_PRIVATE_REGISTRY=""
FROM ${BASE_PRIVATE_REGISTRY}python:3.7.4-slim
LABEL maintainer="yehiyam@gmail.com"
ADD ./requirements.txt /hkube/algorithm-example-python/requirements.txt
WORKDIR /hkube/algorithm-example-python/
RUN pip install -r requirements.txt
COPY . /hkube/algorithm-example-python
CMD ["python3","-u", "app.py"]