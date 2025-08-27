FROM mcr.microsoft.com/devcontainers/javascript-node:20-bullseye AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

FROM mcr.microsoft.com/devcontainers/base:bullseye
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
RUN echo 'events { worker_connections 1024; }\nhttp {\n    include /etc/nginx/mime.types;\n    default_type application/octet-stream;\n    sendfile on;\n    keepalive_timeout 65;\n    include /etc/nginx/conf.d/*.conf;\n}' > /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
