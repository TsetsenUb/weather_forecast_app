FROM python:3.13-alpine

ENV HOME=/home/backend \
    APP_HOME=/home/backend/app \
    PYTHONPATH="$PYTHONPATH:/home/backend" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p $APP_HOME \
    && addgroup -S backend \
    && adduser -S backend_user -G backend

WORKDIR $HOME

COPY ./requirements.txt .

RUN pip install --upgrade pip==25.3 \
    && pip install --no-cache-dir -r requirements.txt

COPY app app

RUN chown -R backend_user:backend $HOME

USER backend_user
