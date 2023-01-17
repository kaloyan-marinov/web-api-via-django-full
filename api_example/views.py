# The Django REST Framework makes it possible to implement request-handling functions
# in a function-based way or in a class-based way,
# as per the following section from the framework's official documentation:
# https://www.django-rest-framework.org/tutorial/2-requests-and-responses/#wrapping-api-views .
# The following statement imports a symbol, which
# makes it possible to implement request-handling functions in a class-based way.
from rest_framework import viewsets, permissions
from .models import Paradigm, Language, Programmer
from .serializers import ParadigmSerializer, LanguageSerializer, ProgrammerSerializer


class ParadigmView(viewsets.ModelViewSet):
    queryset = Paradigm.objects.all()
    serializer_class = ParadigmSerializer
    # permission_classes = (
    #     # permissions.IsAuthenticatedOrReadOnly,
    #     permissions.IsAuthenticated,
    # )


class LanguageView(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ProgrammerView(viewsets.ModelViewSet):
    queryset = Programmer.objects.all()
    serializer_class = ProgrammerSerializer
