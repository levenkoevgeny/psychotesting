# syntax=docker/dockerfile:1
FROM node:16-alpine
RUN npm install -g serve
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build