```
$ cp .env.template .env
# Edit the content of `.env` as per the comments/instructions therein.
```

the remainder of this description will explain how to
use `localhost` (= the local network interface) to serve the Django application

---

```
$ python3 --version
Python 3.8.3

$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

```
# Launch one terminal instance and, in it, start serving the application:

(venv) $ python manage.py runserver
```

```
# Launch a second terminal instance and, in it, issue requests to the application:

$ http localhost:8000/api/

HTTP/1.1 200 OK
Allow: OPTIONS, GET
Content-Length: 26
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Thu, 12 Jan 2023 19:10:58 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "message": "Hello world!"
}
```
