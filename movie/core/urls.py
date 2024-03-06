from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'core'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', intro, name='intro'),
    path('home/', MainPage.as_view(), name='main'),
    path('movies/<int:movie_id>/', MovieDetailsView.as_view(), name='movie_details'),
    path('trends-movies', TrendsListView.as_view(), name='trends'),
    path('user-movies/', UserMovieListView.as_view(), name='user_movies'),
    path('test/create-users_management', create_test_data, name='test'),
    path('about-us/', about_us, name='about_us')

]
