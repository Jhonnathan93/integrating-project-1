from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from book.models import History
from .methods import * 


@user_passes_test(lambda u: u.is_staff)
def reports(request):
    
    categories = {'Fantasía':0, 'Romance':0, 'Historia':0, 'Suspenso':0, 'Autoayuda':0, 'Ciencia Ficción':0}
    topics = {'Biografía':0, 'Novela':0, 'Científico':0, 'Poesía':0}

    all_history_objects = History.objects.all()
    for history_obj in all_history_objects:
        for category in history_obj.topics.split(', '): categories[category] += 1
        for topic in history_obj.genres.split(', '): topics[topic] += 1

    plot_categories(categories)
    plot_genres(topics)

    return render(request, 'reports.html')