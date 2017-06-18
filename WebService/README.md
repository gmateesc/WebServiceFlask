# A web service built using Flask framework

## Table of contents

- [Overview](#p0)

- [Layout of the application](#p1)

- [Configuring the application](#p1a)

- [Starting the web application](#p1b)

- [Example POST and GET requests](#p2)
  - [Example POST request](#p21)
  - [Example GET request](#p22)

- [Causing an exception in the web service](#p3)




<a name="p0" id="p0"></a>
## Overview


The web service [schedule_service.py](https://github.com/DoodleScheduling/devops-gabriel-mateescu/blob/master/WebService/schedule_service.py) is a Python 2.6+ application that provides a REST API as follows:

- the first endpoint /schedule/api/v1/events accepts POST requests with a JSON payload with the format shown below and writes these documents to disk:
```json
{
  "id": "abc123",
  "initiator": {
    "email": "joe.doe@example.com",
    "name": "Joe Doe",
    "notify": false
  },
  "state": "OPEN",
  "title": "Party 3"
}
```

- the second endpoint /schedule/api/v1/events/<event_id> accepts GET requests with an "id" parameter and returns  JSON response with the document.




<a name="p1" id="p1"></a>
## Layout of the application

The layout is shown below:
<p>
<img src="https://github.com/DoodleScheduling/devops-gabriel-mateescu/blob/master/doc/app_layout.png" 
  alt="App layout" width="400">

<p>
The layout includes

- the *schedule_service.py* application

- the helper modules *persistence* and *util*

- the self-signed certificates under *ssl*

- the configuration template *\_\_init\_\_.py.template* from which the file *\_\_init\_\_.py* needs to be generated, e.g., using [Ansible](https://github.com/gmateesc/WebAppDeploymentAutomation/blob/master/README.md#p32). 

- the list packages needed by application *dependencies/requirements.txt*

- documentation about deploying with *Ansible* 





<a name="p1a" id="p1a"></a>
## Configuring the web application


The application is configured by creating an instance of the template *__init__.py.template*.


```shell
$ more conf/__init__.py.template 

# Directory where to save the JSON documents 
#DOCUMENT_ROOT = "/tmp/Schedule/events"

# Location of the SSL certificate and key
#SSL_CERT_DIR  = "/tmp/Schedule/ssl"

# HOST and PORT
#HOST  = "0.0.0.0"
#PORT  = 8888

# Debugging
DEBUG = True
#DEBUG = False
```


The instance *__init__.py* will contain the actual values of the configuration parameters:

- DOCUMENT_ROOT

- SSL_CERT_DIR

- HOST

- PORT

An example of generating the file *__init__.py* using Ansible is given [here](https://github.com/gmateesc/WebAppDeploymentAutomation/blob/master/README.md#p32). 







<a name="p1b" id="p1b"></a>
## Starting the web application


A startup script called *schedule_service.sh* is created when the application is deployed with 
Ansible, as shown [here](https://github.com/gmateesc/WebAppDeploymentAutomation/blob/master/README.md#p13)


Then the application can be started with
```shell
schedule_service.sh start
```





<a name="p2" id="p2"></a>
## Example POST and GET requests



<a name="p21" id="p21"></a>
## Example POST request


```json
  $ curl -k                   \
      -X POST                 \
      -H "Content-Type: application/json"         \
     https://0.0.0.0:8888/schedule/api/v1/events  \
    -d '{
      "id": "13",
      "title": "Party 3",
      "initiator": { "name": "Joe Doe", "notify": false, "email": "joe.doe@example.com" },
       "state": "OPEN"
    }'
  {
    "id": "13",
    "initiator": {
      "email": "joe.doe@example.com",
      "name": "Joe Doe",
      "notify": false
    },
    "state": "OPEN",
    "title": "Party 3"
  }
```






<a name="p22" id="p22"></a>
## Example GET request

```json
  $ curl -k https://0.0.0.0:8888/schedule/api/v1/events/13
  {
    "event": {
      "id": "13",
      "initiator": {
         "email": "joe.doe@example.com",
         "name": "Joe Doe",
         "notify": false
    },
      "state": "OPEN",
      "title": "Party 3"
    }
  }
```




<a name="p3" id="p3"></a>
## Causing an exception in the web service


An exception in the web service can be caused by write proecting the directory where the web service saves the posted JSON documents. For example, 
```script
  $ chmod -w /tmp/Scheduler_app/app/status
```


Then POST-ing a JSON document will cause an exception as follows:



```script
  $ curl -ik                    \
       -X POST                  \
       -H "Content-Type: application/json"     \
       https://0.0.0.0:8888/schedule/api/v1/events  \
     -d '{
      "id": "13",
      "title": "Party 3",
      "initiator": { "name": "Joe Doe", "notify": false, "email": "joe.doe@example.com" },
       "state": "OPEN"
    }'

HTTP/1.0 500 INTERNAL SERVER ERROR
Content-Type: text/html; charset=utf-8
X-XSS-Protection: 0
Connection: close
Server: Werkzeug/0.12.2 Python/2.7.10
Date: Mon, 29 May 2017 07:01:27 GMT

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
  "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <title>IOError: [Errno 13] Permission denied: u'/tmp/Scheduler_app/app/status/13.json' // Werkzeug Debugger</title>


...


<!--

Traceback (most recent call last):
  File "/private/tmp/Scheduler_app/venv/lib/python2.7/site-packages/flask/app.py", line 1997, in __call__
    return self.wsgi_app(environ, start_response)
  File "/private/tmp/Scheduler_app/venv/lib/python2.7/site-packages/flask/app.py", line 1985, in wsgi_app
    response = self.handle_exception(e)
  File "/private/tmp/Scheduler_app/venv/lib/python2.7/site-packages/flask/app.py", line 1540, in handle_exception
    reraise(exc_type, exc_value, tb)
  File "/private/tmp/Scheduler_app/venv/lib/python2.7/site-packages/flask/app.py", line 1982, in wsgi_app
    response = self.full_dispatch_request()
  File "/private/tmp/Scheduler_app/venv/lib/python2.7/site-packages/flask/app.py", line 1614, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/private/tmp/Scheduler_app/venv/lib/python2.7/site-packages/flask/app.py", line 1517, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "/private/tmp/Scheduler_app/venv/lib/python2.7/site-packages/flask/app.py", line 1612, in full_dispatch_request
    rv = self.dispatch_request()
  File "/private/tmp/Scheduler_app/venv/lib/python2.7/site-packages/flask/app.py", line 1598, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "/private/tmp/Scheduler_app/app/WebService/schedule_service.py", line 78, in create_event
    util.save_event(app.config, events, event)
  File "/private/tmp/Scheduler_app/app/WebService/util/__init__.py", line 61, in save_event
    load_store.store_file(file_name, event)
  File "/private/tmp/Scheduler_app/app/WebService/persistence/load_store.py", line 36, in store_file
    with open(file_name, 'w') as json_file:
IOError: [Errno 13] Permission denied: u'/tmp/Scheduler_app/app/status/13.json'

-->
curl: (56) SSLRead() return error -9806
```



