#!/bin/sh
echo "DEBUG: restarting haproxy"
if [ -f /var/run/haproxy.pid ]; then
  haproxy -f /etc/haproxy/haproxy.cfg -p /var/run/haproxy.pid -D -st "$(cat /var/run/haproxy.pid)"
else 
  haproxy -f /etc/haproxy/haproxy.cfg -p /var/run/haproxy.pid
fi
