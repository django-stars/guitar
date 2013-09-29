import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import Chord


def api_chord_search(request, q):
    chords = Chord.active.filter(title__icontains=q).values_list('title', flat=True)
    data = {
        'status': 'OK',
        'chords': list(chords),
    }
    return HttpResponse(json.dumps(data), content_type='application/json')


def api_chord_config(request, title):
    chord = get_object_or_404(Chord.active, title=title)
    return HttpResponse(chord.configuration, content_type='application/json')
