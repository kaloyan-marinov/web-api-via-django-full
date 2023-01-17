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

(

OPTIONALLY, verify that the previous step did create the following tables:

```
$ docker container exec -it container-w-a-v-d-postgres /bin/bash
root@<container-id> psql \
    --host=localhost \
    --port=5432 \
    --username=<the-value-for-POSTGRES_USER-in-the-.env-file> \
    --password \
    <the-value-for-POSTGRES_DB-in-the-.env-file>
<the-value-for-POSTGRES_DB-in-the-.env-file>=# \d
                             List of relations
 Schema |                  Name                   |   Type   |    Owner    
--------+-----------------------------------------+----------+-------------
 public | api_example_language                    | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | api_example_language_id_seq             | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | api_example_paradigm                    | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | api_example_paradigm_id_seq             | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | api_example_programmer                  | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | api_example_programmer_id_seq           | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | api_example_programmer_languages        | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | api_example_programmer_languages_id_seq | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_group                              | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_group_id_seq                       | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_group_permissions                  | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_group_permissions_id_seq           | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_permission                         | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_permission_id_seq                  | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_user                               | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_user_groups                        | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_user_groups_id_seq                 | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_user_id_seq                        | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_user_user_permissions              | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | auth_user_user_permissions_id_seq       | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | django_admin_log                        | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | django_admin_log_id_seq                 | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | django_content_type                     | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | django_content_type_id_seq              | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | django_migrations                       | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | django_migrations_id_seq                | sequence | <the-value-for-POSTGRES_USER-in-the-.env-file>
 public | django_session                          | table    | <the-value-for-POSTGRES_USER-in-the-.env-file>
(27 rows)
```

)

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

HTTP/1.1 403 Forbidden
Allow: GET, HEAD, OPTIONS
Content-Length: 58
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:37:33 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "detail": "Authentication credentials were not provided."
}



$ python manage.py createsuperuser

# Respond to the prompts.

$ export USERNAME=<enter-the-username-that-you-provided-while-responding-to-the-prompts>
$ export PASSWORD=<enter-the-password-that-you-provided-while-responding-to-the-prompts>



$  http \
    --auth ${USERNAME}:${PASSWORD} \
    localhost:8000/api/

HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Length: 158
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:41:34 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "languages": "http://localhost:8000/api/languages/",
    "paradigms": "http://localhost:8000/api/paradigms/",
    "programmers": "http://localhost:8000/api/programmers/"
}



$ http \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/paradigms/ \
    name=procedural

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 75
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:48:36 GMT
Location: http://localhost:8000/api/paradigms/1/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 1,
    "name": "procedural",
    "url": "http://localhost:8000/api/paradigms/1/"
}

$ http \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/paradigms/ \
    name=functional

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 75
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:52:28 GMT
Location: http://localhost:8000/api/paradigms/2/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 2,
    "name": "functional",
    "url": "http://localhost:8000/api/paradigms/2/"
}

$ http \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/paradigms/ \
    name=object-orientedddd

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 83
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:52:50 GMT
Location: http://localhost:8000/api/paradigms/3/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 3,
    "name": "object-orientedddd",
    "url": "http://localhost:8000/api/paradigms/3/"
}



$ http \
    --auth ${USERNAME}:${PASSWORD} \
    PUT localhost:8000/api/paradigms/3/ \
    name=object-orienteD

HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 80
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:53:29 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 3,
    "name": "object-orienteD",
    "url": "http://localhost:8000/api/paradigms/3/"
}

$ http \
    --auth ${USERNAME}:${PASSWORD} \
    PATCH localhost:8000/api/paradigms/3/ \
    name=object-oriented

HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 80
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:54:02 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 3,
    "name": "object-oriented",
    "url": "http://localhost:8000/api/paradigms/3/"
}



$ http \
    --auth ${USERNAME}:${PASSWORD} \
    localhost:8000/api/paradigms/

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 234
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:54:32 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "id": 1,
        "name": "procedural",
        "url": "http://localhost:8000/api/paradigms/1/"
    },
    {
        "id": 2,
        "name": "functional",
        "url": "http://localhost:8000/api/paradigms/2/"
    },
    {
        "id": 3,
        "name": "object-oriented",
        "url": "http://localhost:8000/api/paradigms/3/"
    }
]



$ http \
    --auth ${USERNAME}:${PASSWORD} \
    DELETE localhost:8000/api/paradigms/2/

HTTP/1.1 204 No Content
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 0
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:55:12 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

$ http \
    --auth ${USERNAME}:${PASSWORD} \
    localhost:8000/api/paradigms/

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 158
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:55:31 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

[
    {
        "id": 1,
        "name": "procedural",
        "url": "http://localhost:8000/api/paradigms/1/"
    },
    {
        "id": 3,
        "name": "object-oriented",
        "url": "http://localhost:8000/api/paradigms/3/"
    }
]



$ http \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/languages/ \
    name=C \
    paradigm=http://localhost:8000/api/paradigms/1/

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 118
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:56:17 GMT
Location: http://localhost:8000/api/languages/1/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 1,
    "name": "C",
    "paradigm": "http://localhost:8000/api/paradigms/1/",
    "url": "http://localhost:8000/api/languages/1/"
}

$ http \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/languages/ \
    name=Jave \
    paradigm=http://localhost:8000/api/paradigms/3/

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 121
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:56:36 GMT
Location: http://localhost:8000/api/languages/2/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 2,
    "name": "Jave",
    "paradigm": "http://localhost:8000/api/paradigms/3/",
    "url": "http://localhost:8000/api/languages/2/"
}

$ http \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/languages/ \
    name=PHP \
    paradigm=http://localhost:8000/api/paradigms/1/

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 120
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:56:50 GMT
Location: http://localhost:8000/api/languages/3/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 3,
    "name": "PHP",
    "paradigm": "http://localhost:8000/api/paradigms/1/",
    "url": "http://localhost:8000/api/languages/3/"
}

$ http \
    --auth ${USERNAME}:${PASSWORD} \
    PUT localhost:8000/api/languages/2/ \
    name=Java

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 40
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:57:38 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "paradigm": [
        "This field is required."
    ]
}

$ http \
    --auth ${USERNAME}:${PASSWORD} \
    PATCH localhost:8000/api/languages/2/ \
    name=Java

HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 121
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:58:26 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 2,
    "name": "Java",
    "paradigm": "http://localhost:8000/api/paradigms/3/",
    "url": "http://localhost:8000/api/languages/2/"
}



$ http \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/programmers/ \
    name=Anthony

HTTP/1.1 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 41
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 05:59:28 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "languages": [
        "This field is required."
    ]
}

$ http --verbose \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/programmers/ \
    name=Anthony \
    languages:='["http://localhost:8000/api/languages/1/", "http://localhost:8000/api/languages/2/"]'

POST /api/programmers/ HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Authorization: Basic amQ6MTIz
Connection: keep-alive
Content-Length: 118
Content-Type: application/json
Host: localhost:8000
User-Agent: HTTPie/2.6.0

{
    "languages": [
        "http://localhost:8000/api/languages/1/",
        "http://localhost:8000/api/languages/2/"
    ],
    "name": "Anthony"
}


HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 170
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 06:00:07 GMT
Location: http://localhost:8000/api/programmers/1/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 1,
    "languages": [
        "http://localhost:8000/api/languages/1/",
        "http://localhost:8000/api/languages/2/"
    ],
    "name": "Anthony",
    "url": "http://localhost:8000/api/programmers/1/"
}

$ http --verbose \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/programmers/ \
    name=Stacy \
    languages:='["http://localhost:8000/api/languages/2/", "http://localhost:8000/api/languages/3/"]'

POST /api/programmers/ HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Authorization: Basic amQ6MTIz
Connection: keep-alive
Content-Length: 116
Content-Type: application/json
Host: localhost:8000
User-Agent: HTTPie/2.6.0

{
    "languages": [
        "http://localhost:8000/api/languages/2/",
        "http://localhost:8000/api/languages/3/"
    ],
    "name": "Stacy"
}


HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 168
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 06:01:28 GMT
Location: http://localhost:8000/api/programmers/2/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 2,
    "languages": [
        "http://localhost:8000/api/languages/3/",
        "http://localhost:8000/api/languages/2/"
    ],
    "name": "Stacy",
    "url": "http://localhost:8000/api/programmers/2/"
}

$ http --verbose \
    --auth ${USERNAME}:${PASSWORD} \
    POST localhost:8000/api/programmers/ \
    name=Zoe \
    languages:='["http://localhost:8000/api/languages/1/", "http://localhost:8000/api/languages/2/", "http://localhost:8000/api/languages/3/"]'
POST /api/programmers/ HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Authorization: Basic amQ6MTIz
Connection: keep-alive
Content-Length: 156
Content-Type: application/json
Host: localhost:8000
User-Agent: HTTPie/2.6.0

{
    "languages": [
        "http://localhost:8000/api/languages/1/",
        "http://localhost:8000/api/languages/2/",
        "http://localhost:8000/api/languages/3/"
    ],
    "name": "Zoe"
}


HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 207
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 06:02:14 GMT
Location: http://localhost:8000/api/programmers/3/
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "id": 3,
    "languages": [
        "http://localhost:8000/api/languages/1/",
        "http://localhost:8000/api/languages/3/",
        "http://localhost:8000/api/languages/2/"
    ],
    "name": "Zoe",
    "url": "http://localhost:8000/api/programmers/3/"
}



$ http --verbose \
    --auth ${USERNAME}:${PASSWORD} \
    DELETE localhost:8000/api/programmers/2/

DELETE /api/programmers/2/ HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Authorization: Basic amQ6MTIz
Connection: keep-alive
Content-Length: 0
Host: localhost:8000
User-Agent: HTTPie/2.6.0



HTTP/1.1 204 No Content
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 0
Cross-Origin-Opener-Policy: same-origin
Date: Tue, 17 Jan 2023 06:03:05 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.3
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```
