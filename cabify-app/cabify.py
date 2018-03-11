#!/usr/bin/env python

from bottle import route, run
import socket
import consul
import os

# These are the envs
consul_ip = os.getenv("CONSUL_IP")
consul_port = int(os.getenv("CONSUL_PORT"))
app_name = os.getenv("APP_NAME")
app_port = int(os.getenv("APP_PORT"))
host_ip = os.getenv("HOST_IP")
host_ip = socket.gethostbyname(socket.gethostname())
#ip = socket.gethostbyname(socket.gethostname())
c = consul.Consul(host=consul_ip, port=consul_port)
c.agent.service.register(app_name, service_id="docker-"+app_name+"-"+str(app_port), address=host_ip, port=app_port, http="http://"+host_ip+":"+str(app_port)+"/status", interval="10s", tags=['python'])

@route('/status')
def status():
    return 'OK from '+host_ip+'\n'

run(host='0.0.0.0', port=app_port, debug=False)

