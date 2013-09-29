from django.db import models

class Chord(models.Model):
    # We are safe to use title as slug as it is not possible to have
    # package name, which is not URL friendly (txh: PyPI)
    title = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    configuration = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # Stats, meta info, etc -> as soon as main goals of `guitar` will be solved.

    def __unicode__(self):
        return self.title