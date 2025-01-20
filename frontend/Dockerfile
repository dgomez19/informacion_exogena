# develop stage
FROM node:20-alpine as develop-stage

WORKDIR /app

COPY package*.json ./

RUN yarn global add @quasar/cli

COPY . .

EXPOSE 8080

CMD yarn install && yarn dev --port 8080

# build stage
FROM develop-stage as build-stage

RUN yarn install && quasar build

# production stage
FROM nginx:1.15.7-alpine as production-stage

RUN mkdir /app

COPY --from=build-stage /app/dist/spa /etc/nginx/html

EXPOSE 80

CMD nginx -g 'daemon off;'
