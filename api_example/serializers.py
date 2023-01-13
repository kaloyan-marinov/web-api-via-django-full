from rest_framework import serializers
from .models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = (
            "id",
            "name",
            "paradigm",
        )
        # The previous statement can be replaced with:
        # fmt: off
        '''
        fields = "__all__"
        '''
        # fmt: on
