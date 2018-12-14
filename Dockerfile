FROM python:3.7-slim
COPY dialogclassifier /
COPY requirements.txt /
RUN apt-get update && \
    apt-get install -y gcc g++ unixodbc-dev && \
    pip install -r /requirements.txt  && \
    apt-get remove -y gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean -y
EXPOSE 8000
CMD gunicorn dialogclassifier.wsgi --bind 0.0.0.0:8000
