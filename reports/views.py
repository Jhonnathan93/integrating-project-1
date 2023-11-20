from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from book.models import History
from .methods import * 

"""
@user_passes_test(lambda u: u.is_staff)
def reports(request):

    initial_date = request.GET.get('fecha_inicio')
    print(initial_date)
    final_date = request.GET.get('fecha_fin')
    print(final_date)

    if initial_date and final_date:

        categories = {'Fantasía':0, 'Romance':0, 'Historia':0, 'Suspenso':0, 'Autoayuda':0, 'Ciencia Ficción':0}
        topics = {'Biografía':0, 'Novela':0, 'Científico':0, 'Poesía':0}

        histories = History.objects.filter(date__range=(initial_date, final_date))

        for history_obj in histories:
            print(history_obj.date)

            for category in history_obj.topics.split(', '): categories[category] += 1
            for topic in history_obj.genres.split(', '): topics[topic] += 1

        plot_categories(categories)
        plot_genres(topics)

        return render(request, 'reports.html', {'message': f'Este reporte ha sido creado con los historiales entre {initial_date} y {final_date}.'})

    else: 

        categories = {'Fantasía':0, 'Romance':0, 'Historia':0, 'Suspenso':0, 'Autoayuda':0, 'Ciencia Ficción':0}
        topics = {'Biografía':0, 'Novela':0, 'Científico':0, 'Poesía':0}

        all_history_objects = History.objects.all()
        for history_obj in all_history_objects:
            print(history_obj.date)
            for category in history_obj.topics.split(', '): categories[category] += 1
            for topic in history_obj.genres.split(', '): topics[topic] += 1

        plot_categories(categories)
        plot_genres(topics)

        return render(request, 'reports.html', {'message': 'Este reporte ha sido creado con todos los historiales en la base de datos.'})
        """

def get_date_range(request):
    initial_date = request.GET.get('fecha_inicio')
    final_date = request.GET.get('fecha_fin')
    return initial_date, final_date

def update_counters(histories, categories, topics):
    for history_obj in histories:
        print(history_obj.date)
        for category in history_obj.topics.split(', '):
            categories[category] += 1
        for topic in history_obj.genres.split(', '):
            topics[topic] += 1

def generate_reports(request, initial_date, final_date):
    categories = {'Fantasía': 0, 'Romance': 0, 'Historia': 0, 'Suspenso': 0, 'Autoayuda': 0, 'Ciencia Ficción': 0}
    topics = {'Biografía': 0, 'Novela': 0, 'Científico': 0, 'Poesía': 0}

    histories = History.objects.filter(date__range=(initial_date, final_date))

    update_counters(histories, categories, topics)
    plot_categories(categories)
    plot_genres(topics)

    return render(request, 'reports.html', {'message': f'Este reporte ha sido creado con los historiales entre {initial_date} y {final_date}.'})

@user_passes_test(lambda u: u.is_staff)
def reports(request):
    initial_date, final_date = get_date_range(request)

    if initial_date and final_date:
        return generate_reports(request, initial_date, final_date)
    else:
        categories = {'Fantasía': 0, 'Romance': 0, 'Historia': 0, 'Suspenso': 0, 'Autoayuda': 0, 'Ciencia Ficción': 0}
        topics = {'Biografía': 0, 'Novela': 0, 'Científico': 0, 'Poesía': 0}

        all_history_objects = History.objects.all()
        update_counters(all_history_objects, categories, topics)

        plot_categories(categories)
        plot_genres(topics)

        return render(request, 'reports.html', {'message': 'Este reporte ha sido creado con todos los historiales en la base de datos.'})
