# The Django REST Framework makes it possible to implement request-handling functions
# in a function-based way or in a class-based way,
# as per the following section from the framework's official documentation:
# https://www.django-rest-framework.org/tutorial/2-requests-and-responses/#wrapping-api-views .
# The following statement imports a symbol, which
# makes it possible to implement request-handling functions in a function-based way.
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def hello_world(request):
    data = {
        "message": "Hello world!",
    }
    return Response(data)
