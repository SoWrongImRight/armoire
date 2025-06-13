# Stage 1: Build the React application
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies using Yarn
COPY package.json yarn.lock ./
RUN yarn install

# Copy source and build the app
COPY . .
RUN yarn build

# Stage 2: Serve the built app with nginx
FROM nginx:alpine

# Copy built React files to nginx's public folder
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/build /usr/share/nginx/html

# Optional: custom nginx config
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
