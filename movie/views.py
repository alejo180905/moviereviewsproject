from django.shortcuts import render
from .models import Movie
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter


def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})


def about(request):
    return render(request, 'about.html')


def statistics_view(request):
    movies = Movie.objects.all()

    # Películas por año
    years = [m.year for m in movies if m.year]
    count_by_year = Counter(years)
    years_sorted = sorted(count_by_year.items())
    x_years = [str(y) for y, _ in years_sorted]
    y_counts = [c for _, c in years_sorted]

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.bar(x_years, y_counts, color='tab:blue')
    ax1.set_title('Películas por año')
    ax1.set_xlabel('Año')
    ax1.set_ylabel('Cantidad')
    fig1.tight_layout()

    buf1 = io.BytesIO()
    fig1.savefig(buf1, format='png')
    buf1.seek(0)
    img_year = base64.b64encode(buf1.read()).decode('utf-8')
    buf1.close()
    plt.close(fig1)

    # Películas por género (primer género si hay comas)
    genres_raw = []
    for m in movies:
        if m.genre:
            first = m.genre.split(',')[0].strip()
            if first:
                genres_raw.append(first)
    count_by_genre = Counter(genres_raw)
    top_genres = count_by_genre.most_common()

    labels = [g for g, _ in top_genres]
    values = [c for _, c in top_genres]

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.bar(labels, values, color='tab:orange')
    ax2.set_title('Películas por género (primer género)')
    ax2.set_xlabel('Género')
    ax2.set_ylabel('Cantidad')
    plt.xticks(rotation=45, ha='right')
    fig2.tight_layout()

    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    img_genre = base64.b64encode(buf2.read()).decode('utf-8')
    buf2.close()
    plt.close(fig2)

    return render(request, 'statistics.html', {
        'img_year': img_year,
        'img_genre': img_genre,
    })


def signup(request):
    email = request.GET.get('email', '')
    return render(request, 'signup.html', {'email': email})
    