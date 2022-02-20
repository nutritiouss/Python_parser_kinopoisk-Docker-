FROM python:3.9
MAINTAINER VladimirTikhonov

WORKDIR /usr/project

ENV TYPE_MODEL=news

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

CMD
