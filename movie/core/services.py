import requests
from django.contrib.auth.models import User
from .models import UserMovie

api_key = "e848463ff31c337c7c270d4cf203c82e"


def search(query):
    data = requests.get(
        f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&page=1&include_adult=false&query={query}")

    return data.json()


def get_popular_movies():
    response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}")
    data = response.json()
    movies = data["results"]
    return movies


def get_movie(movie_id):
    data = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US")
    return data.json()


class GetUserMovie:
    def __init__(self, user):
        self.user = user

    def get_ids(self):
        user_movie_ids = set(movie_id for movie_id in
                             UserMovie.objects.filter(user=self.user).values_list('movieID', flat=True))
        return user_movie_ids

    def get_movies(self):
        user_movies = [get_movie(movie_id) for movie_id in self.get_ids()]
        return user_movies


def get_users_data():
    all_users = User.objects.filter(usermovie__isnull=False).distinct()
    all_user_movie_ids = {}
    for user in all_users:
        all_user_movie_ids[user] = [movie_id for movie_id in
                                    UserMovie.objects.filter(user=user).values_list('movieID', flat=True)]
    return all_user_movie_ids


def calculate_jaccard_similarity(set_target, set_other):
    intersection_size = len(set_target.intersection(set_other))
    union_size = len(set_target.union(set_other))
    similarity = intersection_size / union_size if union_size > 0 else 0

    return similarity


def find_similar_users(target_user, users_dict, k):
    if target_user not in users_dict:
        return []

    target_items = set(users_dict[target_user])
    similarities = [(user, calculate_jaccard_similarity(target_items, set(items))) for user, items in
                    users_dict.items() if user != target_user]

    similarities.sort(key=lambda x: x[1], reverse=True)
    neighbors = similarities[:k]
    return neighbors


def search_algo(user):
    users_dict = get_users_data()
    target_user = user
    k_neighbors = 10

    similar_users = find_similar_users(target_user, users_dict, k_neighbors)


    if not similar_users:
        return {'soulmate': 'None', 'percentage': 0, 'recommendations': []}
    soulmate_user, soulmate_similarity = similar_users[0]

    target_user_movie_ids = GetUserMovie(target_user).get_ids()
    if len(similar_users) > 3:
        soulmates_list = similar_users[:3]
    else:
        soulmates_list = similar_users[:len(similar_users)]

    unique_soulmate_movie_ids = set()
    for details in soulmates_list:
        unique_soulmate_movie_ids.update(GetUserMovie(details[0]).get_ids())

    soulmate_movies = [get_movie(movie_id) for movie_id in unique_soulmate_movie_ids
                       if movie_id not in target_user_movie_ids]
    print(soulmate_movies)

    return {'soulmate': soulmate_user, 'percentage': soulmate_similarity * 100,
            'recommendations': soulmate_movies}
