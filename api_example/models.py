from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=64, unique=True)
    paradigm = models.CharField(max_length=64)

    def __str__(self):
        return f"<Language name='{self.name}'>"
