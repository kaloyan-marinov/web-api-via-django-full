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

---

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
