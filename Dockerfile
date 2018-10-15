FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y python-setuptools python-dev build-essential python-pip
ADD . /
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
ENTRYPOINT ["python", "app.py"]
EXPOSE 8000
