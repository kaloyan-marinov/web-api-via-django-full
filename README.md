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
Content-Length: 43
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 04:56:05 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 1,
    "name": "C",
    "paradigm": "procedural"
}

$ http POST localhost:8000/api/languages/ \
    name=Java \
    paradigm=object-oriented

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 51
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 04:56:28 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 2,
    "name": "Java",
    "paradigm": "object-oriented"
}

$ http POST localhost:8000/api/languages/ \
    name=C++ \
    paradigm=object-orientedddd

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 53
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 04:57:03 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 3,
    "name": "C++",
    "paradigm": "object-orientedddd"
}



$ http PUT localhost:8000/api/languages/3/ \
    paradigm=object-oriented

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 36
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 04:57:55 GMT
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
Content-Length: 50
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 04:58:22 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 3,
    "name": "C++",
    "paradigm": "object-oriented"
}



$ http localhost:8000/api/languages/

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 148
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:00:44 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "id": 1,
        "name": "C",
        "paradigm": "procedural"
    },
    {
        "id": 2,
        "name": "Java",
        "paradigm": "object-oriented"
    },
    {
        "id": 3,
        "name": "C++",
        "paradigm": "object-oriented"
    }
]



$ http DELETE localhost:8000/api/languages/2/

HTTP/1.1 204 No Content
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 0
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:01:21 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

$ http localhost:8000/api/languages/

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 96
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 13 Jan 2023 05:01:49 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "id": 1,
        "name": "C",
        "paradigm": "procedural"
    },
    {
        "id": 3,
        "name": "C++",
        "paradigm": "object-oriented"
    }
]
```
