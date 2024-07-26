# More on RESTful Communication

REST APIs use **Uniform Resource Identifiers (URIs) to address resources**. REST API designers should create URIs that convey a REST API's resource model to the potential clients of the API. When resources are named well, an API is intuitive and easy to use.

# Mod Rewrite with POST requests
To partition API to POST and GET APIs, you need to modify Apache config to include some conditions.
* Open your Apache config file, mine is located in `/etc/apache2/sites-available/000-default.conf`, and add the following with root permission
```xml
RewriteCond %{REQUEST_METHOD} ^POST$ [NC]
RewriteRule robot cgi/test.sh
``` 
The condition specifies how to redirect the address based on the request type. Check [Apache site](https://httpd.apache.org/docs/current/mod/mod_rewrite.html) for more details about `RewriteCond`. 
* Restart your Apache server
* To test POST requests, you cannot use your browser easily because the browser operates mainly on GET part of HTTP (unless you create a custom HTML form to submit data). Try `curl` command (`sudo apt install curl` if you don't have it on your system)
```bash
curl -X POST  '<address>/robot'
```
* Check if you receive correct HTML response. You can use the same command for GET requests (replacing POST by GET). `curl` is quite simpler than `nc` as you don't need to specify HTTP headers. However, it is good to experience low-level interactions, particularly with HTTP protocol, a text-based protocol intended by design to help humans debug easily without sophisticated parsing tools.


# Variables
Now, let's use the regex to have a POST URI that takes any number. Replace the RewriteRule by the following:
```
RewriteRule ^robot/([0-9]*\.?[0-9]*$) cgi/test.sh?data=$1
```
Let's parse it now:
* `^` indicates the beginning of URI, where `$` marks the end. So `robot/` should be the first sequence of letters. `()` means a group of letters and is also used as a placeholder for variables in `mod_rewrite`. `[0-9]` means any number from 0 to 9, `*` means the previous character type (or block) is repeated once or multiple times. `+` means it is repeated 0 or many times. `\` is a skip letter for special characters like `.`. `?` says the previous char or block occurs zero or exactly one time.
* Now, test the URI with a POST request

```
curl -X POST  '<address>/robot/123.23'
```
* The output should be

```
<h1>Hello world from NSR 4.0!</h1>
<h2>My name is XXX </h2>
<h2> data=123.23 is selected</h2>
```
* Try different addresses and see if the regex rule works as intended
```
curl -X POST  '<address>/robot/123.23'
curl -X POST  '<address>/robot/532'
curl -X POST  '<address>/robot/12a3.23'  # Error 404 Not found
```


# Web communication in Python - Client side
It is quite easy to make HTTP requests in python using libraries like `requests`. Below is an example code.
* Lets make a simple GET request to your previously designed API. Create a file, named `req.py`  (or run interatively using ipython or Jupiter notebook )
```python
import requests
url = '<ur server dns>/select/b'
x = requests.get(url)
print(x.text)
```

* If you run `print(x)` you will get HTTP response status code, which follows a standard protocol:
    1.  Informational responses (`100`–`199`)
    2.  Successful responses (`200`–`299`)
    3.  Redirection messages (`300`–`399`)
    4.  Client error responses (`400`–`499`)
    5.  Server error responses (`500`–`599`)
    Check [this link](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#information_responses) for more details.
* You can replace `x = requests.get(url)` by `x = requests.post(url)` to run a POST request.  POST allows attaching additional content to requests. One popular attachment is JSON data, a simple text-based data structure for key-value pairs (and more). So, you may modify the above code to attach content to your request.
```python
myobj = {'somekey': 'somevalue'}
x = requests.post(url, json = myobj)
```

# Web communication in Python - Server side
Instead of relying on bash script (which in many cases is useful for simple application), we will use a fully fledged programming language Python. 
* Create a file `<web root>/cgi/test.py`. 
```bash
sudo touch <web root>/cgi/test.py
```

* Give the the write permission and owner
```bash
cd <web root>/cgi
sudo chown www-data:www-data *
sudo chmod 755 *
```
`*` means all files in Bash.
* Now, you may modify to return a JSON response, which is more convenient response for an API (since apps calling the API can easily parse it, unlike html). We want the output to look like

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: <decided automatically>

{"number":"<received number> * 10"}
```
* You may produce this output using bash script with `cgi/test.sh`, but I'd personally go with a programming language such as Python. Below is an example code, which is self-explanatory

```python
#! /usr/bin/python3
import os

# Parsing QUERY_STRING
q = os.getenv('QUERY_STRING')
num_str = q.split('=')[1]
num = int(num_str) * 10

# Generating HTTP  response with JSON
response = "{\"number\": \"%d\"} "%num
print("Content-Type: application/json")
print("Content-Length: %d\n\n"% len(response))
print(response);

```