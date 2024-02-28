FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN groupadd -r adik && useradd -r -g adik adik

WORKDIR /adik

COPY requirements.txt /adik/
RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R adik:adik /adik && chmod 755 /adik

#RUN mkdir /adik/static && /adik/media && chown -R adik:adik /adik && chmod 755 /adik

COPY . /adik/

EXPOSE 8001

CMD python manage.py collectstatic --noinput
