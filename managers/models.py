from django.db import models


class Manager(models.Model):

    name = models.CharField(
        max_length=64,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name
