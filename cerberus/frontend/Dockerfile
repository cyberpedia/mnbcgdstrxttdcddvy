FROM node:20-alpine AS builder
WORKDIR /frontend
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine AS runtime
COPY deploy/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /frontend/dist /usr/share/nginx/html
COPY deploy/nginx/maintenance.html /usr/share/nginx/html/maintenance.html
RUN touch /usr/share/nginx/html/.health && \
    addgroup -S cerberus && adduser -S -G cerberus cerberus && \
    chown -R cerberus:cerberus /var/cache/nginx /var/run /usr/share/nginx/html
USER cerberus
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
