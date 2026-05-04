FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine

WORKDIR /app

RUN apk add --no-cache curl dumb-init

COPY --from=builder /app/node_modules ./node_modules
COPY . .

EXPOSE 3000 3001 3002 3003 3004 9090

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

ENTRYPOINT ["/sbin/dumb-init", "--"]
CMD ["node", "gateway/index.js"]
