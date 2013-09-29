from django.db import models


class ChordManager(models.Manager):
    def get_query_set(self):
        return super(ChordManager, self).get_query_set().filter(is_active=True)


class Chord(models.Model):
    # We are safe to use title as slug as it is not possible to have
    # package name, which is not URL friendly (txh: PyPI)
    title = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    configuration = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ChordManager()

    # Stats, meta info, etc -> as soon as main goals of `guitar` will be solved.

    def __unicode__(self):
        return self.title
