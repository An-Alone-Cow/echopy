FROM python:latest

RUN mkdir -p /monkey/logs/sessions/
EXPOSE 8000

ADD main.py /monkey/
WORKDIR /monkey

ENTRYPOINT ["python3", "main.py"]
