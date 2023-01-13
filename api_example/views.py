# The Django REST Framework makes it possible to implement request-handling functions
# in a function-based way or in a class-based way,
# as per the following section from the framework's official documentation:
# https://www.django-rest-framework.org/tutorial/2-requests-and-responses/#wrapping-api-views .
# The following statement imports a symbol, which
# makes it possible to implement request-handling functions in a class-based way.
from rest_framework import viewsets
from .models import Language
from .serializers import LanguageSerializer


class LanguageView(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
