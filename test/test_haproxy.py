import pytest
import requests
import time
time.sleep(10)

def http_request(url):
  r = requests.get(url)
  return r

def test_good_http_request():
  assert http_request('http://haproxy:8080/status').status_code == 200

def test_bad_http_request():
  assert http_request('http://haproxy:8080/').status_code == 404
