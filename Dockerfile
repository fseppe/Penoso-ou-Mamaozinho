FROM node:14.14.0-alpine as build-vue

RUN mkdir app \
    app/frontend \
    app/backend

ENV PATH /app/frontend/node_modules/.bin:$PATH
COPY ./frontend/package*.json ./app/frontend/
RUN cd app/frontend; npm install
COPY ./frontend ./app/frontend/
RUN cd app/frontend; npm run build

FROM python:3.9.0-slim as build-flask

COPY ./requirements.txt ./app/
RUN apt-get update && apt-get install build-essential -y
RUN apt-get install default-libmysqlclient-dev -y
RUN pip install -r app/requirements.txt
COPY ./backend ./app/backend/
COPY --from=build-vue /app/frontend/templates ./app/frontend/templates
COPY --from=build-vue /app/frontend/templates/static ./app/frontend/templates/static
COPY . ./app/

WORKDIR /app

CMD flask run --host 0.0.0.0 --port $PORT