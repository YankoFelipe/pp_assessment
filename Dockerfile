FROM python:3.9.6-alpine3.14

WORKDIR .

RUN apk update && apk add python3-dev gcc libc-dev build-base

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
