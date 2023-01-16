from django.db import models


class Paradigm(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"<Paradigm name='{self.name}'>"


class Language(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # The following statement suggests that each language can have only 1 paradigm.
    # (In practice, that's not exactly true - b/c a lot of languages can have more than
    # 1 paradigm, but this example will ignore that "slightly more complex" reality.)
    paradigm = models.ForeignKey(Paradigm, on_delete=models.CASCADE)

    def __str__(self):
        return f"<Language name='{self.name}'>"


class Programmer(models.Model):
    name = models.CharField(max_length=64)
    languages = models.ManyToManyField(Language)

    def __str__(self):
        return f"<Programmer name='{self.name}'>"
