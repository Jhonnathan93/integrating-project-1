import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_categories(categories):
    """
    Plot a bar chart for book categories.

    :param categories: Dictionary containing categories as keys and their corresponding values.
    """
    x = []
    y = []
    for key, value in categories.items():
        x.append(key)
        y.append(value)
    
    plt.figure(figsize=(8, 5)) 
    plt.bar(x, y)
    plt.xlabel('Categorías')
    plt.ylabel('Valores')
    plt.title('Gráfica de Categorías')
    plt.savefig("media/reports/categories.png")
    plt.close()

def plot_genres(topics):
    """
    Plot a bar chart for book genres.

    :param topics: Dictionary containing genres as keys and their corresponding values.
    """
    x = []
    y = []
    for key, value in topics.items():
        x.append(key)
        y.append(value)

    plt.figure(figsize=(8, 5))
    plt.bar(x, y)
    plt.xlabel('Géneros')
    plt.ylabel('Valores')
    plt.title('Gráfica de Géneros literarios')
    plt.savefig("media/reports/genres.png")
    plt.close()
