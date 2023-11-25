import requests
from .models import History
from django.contrib.auth.decorators import login_required

@login_required
def save_history(request, _books, _topics, _genres):
    """
    Save user's search history to the database.

    :param request: Django request object.
    :param _books: String representing the books searched.
    :param _topics: String representing the topics related to the search.
    :param _genres: String representing the genres related to the search.
    """
    user_history = History(user=request.user, books=_books, topics=_topics, genres=_genres)
    user_history.save()

def buscar_libros(consulta):
    """
    Search for books using the Google Books API based on a query.

    :param consulta: Query string used to search for books.
    :return: List of dictionaries containing information about found books.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q={consulta}&printType=books&langRestrict=es&maxResults={1}"

    try:
        response = requests.get(url)
        datos = response.json()

        if 'items' not in datos:
            print("No se encontraron libros que coincidan con la consulta.")

        libros_encontrados = []

        for libro in datos['items']:
            info_libro = libro['volumeInfo']
            titulo = info_libro.get('title', 'Título no disponible')
            autores = info_libro.get('authors', ['Autor no disponible'])
            descripcion = info_libro.get('description', 'Sin descripción disponible.')
            imagen_enlace = info_libro['imageLinks']['thumbnail']
            buy_link = info_libro.get('infoLink', 'Enlace de compra no disponible')
            lenguaje = info_libro.get('language', 'Lenguaje no disponible')
            categoria = info_libro.get('categories', ['Categoría no disponible'])
            paginas = info_libro.get('pageCount', 'Número de páginas no disponible')
            fecha_publicacion = info_libro.get('publishedDate', 'Fecha de publicación no disponible')

            libro_info = {
                'titulo': titulo,
                'autores': autores,
                'descripcion': descripcion,
                'imagen_enlace': imagen_enlace,
                'buy_link': buy_link,
                'lenguaje': lenguaje,
                'categoria': ', '.join(categoria),
                'paginas': paginas,
                'fecha_publicacion': fecha_publicacion
            }
            libros_encontrados.append(libro_info)

        return libros_encontrados        

    except Exception as e:
        print(f"Se produjo un error: {str(e)}")
        return None
