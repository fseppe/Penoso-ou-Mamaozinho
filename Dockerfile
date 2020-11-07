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

COPY --from=build-vue /app/frontend/templates ./app/frontend/templates
COPY --from=build-vue /app/frontend/templates/static ./app/frontend/templates/static
RUN apt update && apt install build-essential libpq-dev -y
COPY ./requirements.txt ./app/
RUN pip install -r app/requirements.txt
COPY . ./app/
COPY ./backend ./app/backend/

WORKDIR /app

CMD flask run --host 0.0.0.0 --port $PORT
