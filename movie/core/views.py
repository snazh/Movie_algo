import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import AddCommentForm
from .models import *
from .services import *
import requests

api_key = "e848463ff31c337c7c270d4cf203c82e"


class MainPage(View):
    def get(self, request):
        context = {
            'title': 'Main page',
        }
        # Get popular movies
        query = request.GET.get('q')

        if query:
            context['search_results'] = search(query)

        if request.user.is_authenticated:
            # Get recommendations
            recommendations_data = search_algo(self.request.user)
            context['recommendations'] = recommendations_data['recommendations']
            context['percentage'] = recommendations_data['percentage']
            context['soulmate'] = recommendations_data['soulmate']

        return render(request, 'core/main_page.html', context=context)


class TrendsListView(View):
    def get(self, request):
        trends = get_popular_movies()
        context = {
            'title': 'Trends',
            'popular_movies': trends,

        }
        return render(request, 'core/popular_movies.html', context=context)


class UserMovieListView(View):
    def get(self, request):

        user_movies = GetUserMovie(self.request.user).get_movies()
        context = {
            'title': 'My movies',
            'user_movies': user_movies
        }
        return render(request, 'core/user_movies.html', context=context)


class MovieDetailsView(View):
    def get(self, request, movie_id):
        data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
        try:
            UserMovie.objects.get(user=self.request.user, movieID=movie_id)
        except UserMovie.DoesNotExist:
            status = False
        else:
            status = True
        form = AddCommentForm()
        comments = Comment.objects.filter(movieID=movie_id)
        context = {
            "data": data.json(),
            "button_status": status,
            'comments': comments,
            "form": form,
        }
        return render(request, "core/movie_overview.html", context)

    def post(self, request, movie_id):

        if 'add_to_favorite' in request.POST:

            # Check if the movie is already in user's favorites
            try:
                user_movie = UserMovie.objects.get(user=self.request.user, movieID=movie_id)
            except UserMovie.DoesNotExist:
                # If not, create a new entry
                UserMovie.objects.create(user=self.request.user, movieID=movie_id)
            else:
                # If yes, delete the entry
                user_movie.delete()
        if 'add_comment' in request.POST:

            form = AddCommentForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                Comment.objects.create(user=self.request.user, movieID=movie_id, content=content)

        return redirect('core:movie_details', movie_id=movie_id)


def intro(request):
    context = {
        'title': 'Get started',
    }
    return render(request, 'core/intro_page.html', context=context)


def about_us(request):
    context = {
        'title': 'About us'
    }
    return render(request, 'core/about_us.html', context=context)


def create_test_data(request):
    names = [f'user{index}' for index in range(100)]

    movieIDs = [866398, 933131, 609681, 787699, 572802, 940551, 1212073, 1022796, 1072790, 969492, 695721]
    for index, name in enumerate(names, 0):
        User.objects.create(username=name, password='Sk10112005', email=f'{name}@gmail.com')
        randomNum = random.randint(2, 10)
        randomMovieIDs = random.sample(movieIDs, k=randomNum)

        for i in range(randomNum):
            UserMovie.objects.create(user=User.objects.get(username=name), movieID=randomMovieIDs[i])

    return HttpResponse("Successful test")
