import matplotlib.pyplot as plt

def categories():
    categorias = ['Fantasía', 'Romance', 'Historia', 'Suspenso', 'Autoayuda', 'Ciencia Ficción']
    valores = [10, 25, 12, 28, 5, 35]
    plt.figure(figsize = (8, 5)) 

    plt.bar(categorias, valores)

    plt.xlabel('Categorías')
    plt.ylabel('Valores')
    plt.title('Gráfica de Categorías')

    plt.savefig("reports/categories.png")
    plt.close()


def genres():
    categorias = ['Biografía', 'Novela', 'Científico', 'Poesía']
    valores = [26, 22, 12, 19]
    plt.figure(figsize = (6, 5)) 

    plt.bar(categorias, valores)

    plt.xlabel('Géneros')
    plt.ylabel('Valores')
    plt.title('Gráfica de Géneros literarios')

    plt.savefig("reports/genres.png")
    plt.close()

categories()
genres()