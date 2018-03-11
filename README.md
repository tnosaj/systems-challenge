## Part 1: Configuration Management
```
Given the description provided at the beginning of the challenge, the tasks to
be completed in this part are:

- Containerize `cabify` service using Docker.
- Manage the service discovery of the service using Consul.
- Improve the service balancing strategy using HAProxy. There are
   many solutions for this task, some of them combine HAProxy with other
   technologies and you are allowed to do so.

The result of the assignment should have at least two instances of the Cabify
service running and should be accessible from the host via curl just like in
the example above.
```

This was my first experience with docker, so please be kind if I did not 
follow best practices.

Running the assignment:
```
git clone https://github.com/tnosaj/systems-challenge.git
cd system-challenge
docker-compose up
```
This will deploy:
- 1x single instance consul cluser
- 1x haproxy - configured via consul-template
- 2x cabify-app containers - self registration done via `python-consul`
- 1x test container - runs simple python assertion tests

### Consul
Consul exposes its HTTP api on port `8500`:
```
~:  curl -s http://localhost:8500/v1/agent/members|jq
[
  {
    "Name": "216a792bb949",
    "Addr": "172.18.0.2",
    "Port": 8301,
    "Tags": {
      "bootstrap": "1",
      "build": "0.5.2:9a9cc934",
      "dc": "cabify",
      "port": "8300",
      "role": "consul",
      "vsn": "2",
      "vsn_max": "2",
      "vsn_min": "1"
    },
    "Status": 1,
    "ProtocolMin": 1,
    "ProtocolMax": 2,
    "ProtocolCur": 2,
    "DelegateMin": 2,
    "DelegateMax": 4,
    "DelegateCur": 4
  }
]
```

### Haproxy
Consul-template configures haproxy by querying the `cabify` consul service.

The haproxy will answer on port `8080`:
```
~:  curl -Li http://localhost:8080/status
HTTP/1.0 200 OK
Date: Sun, 11 Mar 2018 20:43:47 GMT
Server: WSGIServer/0.2 CPython/3.6.4
Content-Length: 19
Content-Type: text/html; charset=UTF-8
Connection: keep-alive

OK from 172.18.0.3
```
In addition the admin interface is exposed on port `8081`:
```
~:  curl -Li http://localhost:8081/stats\?stats\;csv\;
```
where the 2 app servers have registered on the `cabify` backend:
```
cabify,FRONTEND,,,0,1,10000,3,376,1226,0,0,0,,,,,OPEN,,,,,,,,,1,2,0,,,,0,0,0,2,,,,0,2,0,1,0,0,,0,2,3,,,0,0,0,0,,,,,,,,,,,,,,,,,,,,,http,,0,2,3,0,0,0,
cabify,172.18.0.3-8181,0,0,0,1,,2,233,346,,0,,0,0,0,0,UP,1,1,0,0,0,486,0,,1,3,1,,2,,2,0,,1,L4OK,,0,0,2,0,0,0,0,,,,,0,0,,,,,309,,,0,0,1,1,,,,Layer4 check passed,,2,3,4,,,,172.18.0.3:8181,,http,,,,,,,,
cabify,172.18.0.4-8182,0,0,0,1,,1,143,880,,0,,0,0,0,0,UP,1,1,0,0,0,486,0,,1,3,2,,1,,2,0,,1,L4OK,,0,0,0,0,1,0,0,,,,,0,0,,,,,484,,,0,0,1,1,,,,Layer4 check passed,,2,3,4,,,,172.18.0.4:8182,,http,,,,,,,,
cabify,BACKEND,0,0,0,1,1000,3,376,1226,0,0,,0,0,0,0,UP,2,2,0,,0,486,0,,1,3,0,,3,,1,0,,2,,,,0,2,0,1,0,0,,,,3,0,0,0,0,0,0,309,,,0,0,1,1,,,,,,,,,,,,,,http,roundrobin,,,,,,,
```

### App
The app container does not expose any ports outside the docker-compose 
application. The bottle app auto registers with consul on startup by 
using [python-consul](https://python-consul.readthedocs.io/en/latest/).


### Notes
- Initially I was using consul's dns endpoint to resolve the IP of the 
consul server. This worked well, however as I have dove into docker-compose 
i realized that there is local resolution within a docker-compose 
application scope.

- I spent quite a bit of time trying to find out how to register multiple 
app servers in consul until I was pointed at 
[this](https://github.com/hashicorp/consul/issues/1659#issuecomment-320854604)
link.

- For the auto-registration, I experimented with `registrator`, but opted 
for the application to self register rather than adding an additional error 
source.

- Instead of using the `/status` as a check url, the haproxy uses the simple 
`tcp` health check at a lower interval than the consul service check. This 
means that the haproxy will mark a failed node as down much quicker than 
consul will. Another reason for this was that haproxy seems to prematurely 
close the http socket when executing `GET` and `HEAD` health checks resulting 
in the applications logs being spammed with `BrokenPipeError: [Errno 32] Broken pipe` 
errors.


## Part 2: Questions

```
- Identify the SPOFs in the result of the assignment and explain how you would
  solve them.
```
  

  
```
- Explain how would you upgrade the Cabify service without downtime. We
  would like to have a short term solution, something that in the real world
  you would be able to deliver the same day or week. Then provide an
  explanation for a more complex solution where you improve the state of this
  assignment to your ideal release management process.
```
