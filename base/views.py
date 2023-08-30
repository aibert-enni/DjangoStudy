from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
profiles = [
    {'id': 0, 'name': "Chmo", 'surname': "sosatel"},
    {'id': 1, 'name': "Rock", 'surname': "sosatel"},
    {'id': 2, 'name': "Tomas", 'surname': "sosatel"}
]


def home(request):
    return render(request, 'base/home.html', {'profiles': profiles})

def profile(request, pk):
    profile = None
    for i in profiles:
        if i['id'] == int(pk):
            profile = i

    return render(request, 'base/profile.html', {'profile': profile})