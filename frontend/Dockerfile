# Multi-stage build for production React application
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies with legacy peer deps to avoid conflicts
RUN npm ci --legacy-peer-deps || npm install --legacy-peer-deps

# Copy source code and configuration files
COPY . .

# Build the application (without VITE_API_URL - will be injected at runtime)
RUN npm run build

# Verify build output
RUN ls -la /app/dist

# Production stage with nginx
FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy custom nginx configuration (full config, not just server block)
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy runtime config injection script
COPY inject-config.sh /docker-entrypoint.d/40-inject-config.sh
RUN chmod +x /docker-entrypoint.d/40-inject-config.sh

# Verify files were copied
RUN ls -la /usr/share/nginx/html

# Create a non-root user for nginx
RUN addgroup -g 1001 -S nginx && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx || true

# Set proper permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx && \
    touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid && \
    chmod -R 755 /docker-entrypoint.d

# Expose port 8080 (matching nginx.conf and Code Engine default)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Switch to non-root user
USER nginx

# Use the injection script as entrypoint
CMD ["/docker-entrypoint.d/40-inject-config.sh"]

# Made with Bob
