FROM python:3
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code
CMD ["./start.sh"]
