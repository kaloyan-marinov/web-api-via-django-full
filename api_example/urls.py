from django.urls import path, include
from . import views
from rest_framework import routers


d_r = routers.DefaultRouter()
d_r.register("languages", views.LanguageView)


urlpatterns = [
    path("", include(d_r.urls)),
]
