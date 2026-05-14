#!/bin/sh
# Inject runtime configuration into the built app

# Create runtime config file
cat > /usr/share/nginx/html/config.js << EOF
window.ENV = {
  VITE_API_URL: '${VITE_API_URL}'
};
EOF

echo "Runtime configuration injected:"
cat /usr/share/nginx/html/config.js

# Start nginx
exec nginx -g 'daemon off;'

# Made with Bob
