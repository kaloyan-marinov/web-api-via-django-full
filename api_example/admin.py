from django.contrib import admin
from .models import Language


# All that the following statement does is to make it possible to
# navigate to http://127.0.0.1:8000/admin/
# and see web UI "controls" for creating, editing, and deleting `Language` instances.
admin.site.register(Language)
