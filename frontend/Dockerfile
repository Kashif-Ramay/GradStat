# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies with legacy peer deps
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Build the app (with increased memory for build)
ENV NODE_OPTIONS=--max-old-space-size=4096
RUN npm run build || (cat /root/.npm/_logs/*.log && exit 1)

# Install serve globally
RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
