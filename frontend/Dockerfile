FROM node:21-alpine as builder
WORKDIR /app
COPY ./package*.json .
RUN npm install --omit=dev
COPY . .
RUN npm run build

FROM nginx:stable-alpine3.17-slim
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;" ]
