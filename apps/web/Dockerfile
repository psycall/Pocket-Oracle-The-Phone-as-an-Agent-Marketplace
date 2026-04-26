# Orvion Web — Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runtime
WORKDIR /app
RUN addgroup --system orvion && adduser --system --group orvion
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
USER orvion
EXPOSE 3000
ENV PORT=3000 NODE_ENV=production
CMD ["node", "server.js"]
