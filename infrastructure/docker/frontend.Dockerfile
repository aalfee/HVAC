# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY ../../frontend /app

RUN npm install && npm run build

EXPOSE 3000

CMD ["npm", "run", "preview"]
