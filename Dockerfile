FROM python:3.8

ENV DEBIAN_FRONTEND=noninteractive
ADD . /opt/telegram_bot/
WORKDIR opt/telegram_bot/

RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 8000

CMD [ "python", "./main.py" ]