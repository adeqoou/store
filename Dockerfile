#FROM python:3.12
#
#
#SHELL ["/bin/bash", "-c"]
#
## Не будет создавать файл с кэшом
#ENV PYTHONDONTWRITEBYTECODE 1
## Если произойдет какая-то ошибка выведутся все данные, они не будут буферизированы
#ENV PYTHONUNBUFFERED 1
#
## RUN это тоже самое, что и bin/bash -c pip install --upgrade pip
#RUN pip install --upgrade pip
#
#RUN apt update && apt install -y libpq-dev build-essential libjpeg-dev libpng-dev libssl-dev
#
#RUN useradd -rms /bin/bash adik && chmod 777 /opt /run
#
## WORKDIR-это mkdir и cd, чтобы не хранить файлы в корневой папке, мы создаем другую папку и храним там
#WORKDIR /yt
#
#RUN mkdir /yt/staticfiles && mkdir /yt/media && chown -R adik:adik /yt/staticfiles && chmod -R 755 /yt/staticfiles
#
#COPY --chown=adik:adik . .
#
#RUN pip install -r requirements.txt
#
#USER adik
#
## Запуск контейнера на основе нашего образа
#CMD ["gunicorn", "-b", "0.0.0.0:8000", "my_store.wsgi:application"]
