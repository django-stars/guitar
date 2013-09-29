from django.contrib import admin

from .models import Chord
from .forms import ChordAdminForm

class ChordAdmin(admin.ModelAdmin):
    form = ChordAdminForm
    list_dispay = ('title', 'is_active', 'updated')

    fieldsets = (
        (None, {
            'fields': (('title', 'is_active'),)
        }),
        (None, {
            'fields': ('configuration',)
        })
    )

admin.site.register(Chord, ChordAdmin)