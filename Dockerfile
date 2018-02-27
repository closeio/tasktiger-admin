FROM python:2-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/mrname/tasktiger-admin.git

WORKDIR tasktiger-admin

RUN python setup.py install

EXPOSE 5000

CMD ["tasktiger-admin", "-i", "0.0.0.0"]
