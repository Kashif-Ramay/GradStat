# Backend Dockerfile
FROM node:18-slim

WORKDIR /srv

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Create necessary directories
RUN mkdir -p uploads results

EXPOSE 3001

CMD ["node", "server.js"]
