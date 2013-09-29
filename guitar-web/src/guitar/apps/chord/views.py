from django.shortcuts import render, get_object_or_404

from .models import Chord


def home(request):
    return render(request, 'home.html')

def chord_list(request):
    chords = Chord.active.all()
    data = {
        'chords': chords
    }
    return render(request, 'chord/list.html', data)

def chord_details(request, title):
    chord = get_object_or_404(Chord.active, title=title)
    data = {
        'chord': chord
    }
    return render(request, 'chord/details.html', data)
