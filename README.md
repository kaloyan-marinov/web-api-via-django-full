```
$ cp .env.template .env

# Edit the content of `.env` as per the comments/instructions therein.
```

the remainder of this description will explain how to
use Docker to serve the persistence layer,
but use `localhost` (= the local network interface) to serve the Django application

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
docker run \
    --name container-w-a-v-d-postgres \
    --mount source=volume-w-a-v-d-postgres,destination=/var/lib/postgresql/data \
    --env-file .env \
    --publish 5432:5432 \
    postgres:15.1
```

(

OPTIONALLY, verify that the previous step did start serving a PostgreSQL server:

```
$ docker container exec -it container-w-a-v-d-postgres /bin/bash
root@<container-id> psql \
    --host=localhost \
    --port=5432 \
    --username=<the-value-for-POSTGRES_USER-in-the-.env-file> \
    --password \
    <the-value-for-POSTGRES_DB-in-the-.env-file>
<the-value-for-POSTGRES_DB-in-the-.env-file>=# \d
Did not find any relations.
```

)

```
(venv) $ python manage.py migrate
```

---

```
# Launch one terminal instance and, in it, start serving the application:

(venv) $ python manage.py runserver
```

```
# Launch a second terminal instance and, in it, issue requests to the application.
# That can be done in many ways:
# (a) go to "the root page of the implemented API"
# which is at http://127.0.0.1:8000/api/ ;
# (b) use the `http` command-line utility;
# (c) other.
# In what follows, we will use option (b).

$ http localhost:8000/api/

HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Length: 52
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 04:53:30 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "languages": "http://localhost:8000/api/languages/"
}



$ http POST localhost:8000/api/languages/ \
    name=C \
    paradigm=procedural

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 90
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:41:46 GMT
Location: http://localhost:8000/api/languages/1/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 1,
    "name": "C",
    "paradigm": "procedural",
    "url": "http://localhost:8000/api/languages/1/"
}

$ http POST localhost:8000/api/languages/ \
    name=Java \
    paradigm=object-oriented

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 98
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:42:15 GMT
Location: http://localhost:8000/api/languages/2/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 2,
    "name": "Java",
    "paradigm": "object-oriented",
    "url": "http://localhost:8000/api/languages/2/"
}

$ http POST localhost:8000/api/languages/ \
    name=C++ \
    paradigm=object-orientedddd

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 100
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:43:01 GMT
Location: http://localhost:8000/api/languages/3/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 3,
    "name": "C++",
    "paradigm": "object-orientedddd",
    "url": "http://localhost:8000/api/languages/3/"
}



$ http PUT localhost:8000/api/languages/3/ \
    paradigm=object-oriented

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 36
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:43:25 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "name": [
        "This field is required."
    ]
}

$ http PATCH localhost:8000/api/languages/3/ \
    paradigm=object-oriented

HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 97
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:44:08 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 3,
    "name": "C++",
    "paradigm": "object-oriented",
    "url": "http://localhost:8000/api/languages/3/"
}



$ http localhost:8000/api/languages/

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 289
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:44:50 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "id": 1,
        "name": "C",
        "paradigm": "procedural",
        "url": "http://localhost:8000/api/languages/1/"
    },
    {
        "id": 2,
        "name": "Java",
        "paradigm": "object-oriented",
        "url": "http://localhost:8000/api/languages/2/"
    },
    {
        "id": 3,
        "name": "C++",
        "paradigm": "object-oriented",
        "url": "http://localhost:8000/api/languages/3/"
    }
]



$ http DELETE localhost:8000/api/languages/2/

HTTP/1.1 204 No Content
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 0
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:45:16 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

$ http localhost:8000/api/languages/

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 190
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:45:29 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "id": 1,
        "name": "C",
        "paradigm": "procedural",
        "url": "http://localhost:8000/api/languages/1/"
    },
    {
        "id": 3,
        "name": "C++",
        "paradigm": "object-oriented",
        "url": "http://localhost:8000/api/languages/3/"
    }
]
```
