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
