import requests


def buscar_libros(consulta, max_resultados=1):
    url = f"https://www.googleapis.com/books/v1/volumes?q={consulta}&maxResults={max_resultados}"

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
            imagen_enlace = info_libro.get('imageLinks', {}).get('small', 'Enlace de imagen no disponible')
            buy_link = info_libro.get('infoLink', 'Enlace de compra no disponible')

            libro_info = {
                'titulo': titulo,
                'autores': autores,
                'descripcion': descripcion,
                'imagen_enlace': imagen_enlace,
                'buy_link': buy_link
            }
            libros_encontrados.append(libro_info)
        
        return libros_encontrados        

    except Exception as e:
        print(f"Se produjo un error: {str(e)}")
        return None