from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Message
import csv
import requests, json
from django.core import serializers
from datetime import datetime, timedelta
from decouple import config
from pprint import pprint
from .models import Movie, Genre, Rating
import random
from .forms import RatingForm, MovieModifyForm, CustomRatingForm
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    user_movies = []
    # if request.user.is_authenticated:
    #     user_movies = Movie.objects.
    messages = []
    if request.user.is_authenticated:
        messages = Message.objects.filter(receive=request.user)
    context = { 'messages': messages, 'user_movies': user_movies }
    return render(request, 'movies/index.html', context)

def genre_page(request):
    user = request.user
    # print('user.like_genres : ',user.like_genres.all().count())
    if not user.is_authenticated:
        return redirect('accounts:login')
    if user.like_genres.all().count() == 0:
        mes = False
    else:
        mes = True
    # print(type(Movie.objects.all()))
    random_movies = random.sample(list(Movie.objects.all()), 10)
    
    context = {'mes': mes, 'random_movies': random_movies}
    return render(request, 'movies/genre_choice.html', context)

@login_required
def main(request):
    movies = []
    movie_ids = [movie.id for movie in Movie.objects.all()]
    l = len(movie_ids)
    nums = list(range(1, l-1))
    randomTeaser = ''
    randomPoster = ''
    movieId = ''
    while len(movies) < 10:
        if not nums:
            break
        num = random.choice(nums)
        movie = get_object_or_404(Movie, pk=movie_ids[num])
        if movie.teaser:
            if len(movies) == 0:
                randomTeaser = movie.teaser
                randomPoster = movie.poster_url
                movieId = movie.pk
            movies.append(movie)
            nums.remove(num)

    allMovies = Movie.objects.all()
    allGenres = {}

    for genre in Genre.objects.all():
        allGenres[genre] = genre.movies.all()
    
    context = {'movies': movies, 'randomTeaser': randomTeaser, 'randomPoster': randomPoster, 
                'allMovies': allMovies, 'allGenres': allGenres, 'movieId': movieId,
            }       
    return render(request, 'movies/main.html', context)

def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    casts = movie.cast_set.all()
    form = RatingForm()
    ratings = movie.ratings_set.all()
    context = {'movie': movie, 'form': form, 'ratings': ratings, 'casts': casts}
    return render(request, 'movies/movie_detail.html', context)

# @login_required
# def rating_create(request, movie_pk):
#     if request.is_ajax():
#         movie = get_object_or_404(Movie, pk=movie_pk)
#         body_unicode = request.body.decode('UTF-8')
#         body = json.loads(body_unicode)
#         rating = Rating()
#         if body['comment'] == '' or body['score'] == None:
#             return HttpResponse('빈 내용 작성 불가')
#         else:
#             rating.comment = body['comment']
#             rating.score = body['score']
#             rating.user = request.user
#             rating.movie = movie
#             rating.save()
#             return HttpResponse('Rating 작성 성공')
#     else:
#         pass

@login_required
def rating_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        print(form)
        if form.is_valid():
            t_form = form.save(commit=False)
            t_form.user = request.user
            t_form.movie_id = movie_pk
            t_form.save()
    else:
        form = RatingForm()
    return redirect('movies:movie_detail', movie_pk)
    
@login_required
def rating_modify(request, movie_pk, rating_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rating = get_object_or_404(Rating, pk=rating_pk, movie_id=movie_pk)
    if rating.user != request.user:
        return redirect('movies:movie_detail', movie_pk)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        form.comment = request.POST.get('comment')
        form.score = request.POST.get('score')
        if form.is_valid():
            print('유효성 통과')
            t_form = form.save(commit=False)
            t_form.user = request.user
            t_form.movie_id = movie_pk
            t_form.save()
    return redirect('movies:movie_detail', movie_pk)
    
    

@login_required
def rating_delete(request, movie_pk, rating_pk):
    rating = get_object_or_404(Rating, movie_id=movie_pk, pk=rating_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    if rating.user == request.user:
        rating.delete()
    return redirect('movies:movie_detail', movie_pk)

@login_required
def movie_modify(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if not request.user.is_superuser:
        return redirect('movies:movie_detail', movie_pk)
    
    if request.method == 'POST':
        form = MovieModifyForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:movie_detail', movie_pk)
    else:
        form = MovieModifyForm(instance=movie, initial={'genres': [genre.id for genre in movie.genres.all()]})
    context = {'form': form}
    return render(request, 'movies/form.html', context)

@login_required
def movie_delete(request, movie_pk):
    if request.user.username != 'admin':
        return redirect('movies:movie_detail', movie_pk)

@login_required 
def like(request, movie_pk):     
    if request.is_ajax():       
        movie = get_object_or_404(Movie, pk=movie_pk)       
        if movie.like_users.filter(pk=request.user.pk).exists():           
            movie.like_users.remove(request.user)           
            liked = False  # 이미 좋아할 시 false 반환     
        else:
            movie.like_users.add(request.user)           
            liked = True  # 새로 좋아할 시 true 반환
        context = {'liked': liked, 'count': movie.like_users.count(),}       
        return JsonResponse(context)     
    else:        
        return HttpResponseBadRequest

@login_required
def addRating(request, movie_pk):
    if not 1<= int(request.POST.get('score')) < 10:
        return redirect('movies:movie_detail')
    if request.is_ajax():
        # print(request.POST.get('comment'))
        movie = get_object_or_404(Movie, pk=movie_pk)
        form = RatingForm(request.POST)
        # form.comment = request.POST.get('comment')
        # form.score = request.POST.get('score')
        print(form)
        # print(list(Rating.objects.filter(movie_id=movie_pk)))
        if form.is_valid():
            print('유효성 통과')
            t_form = form.save(commit=False)
            t_form.movie_id = movie_pk
            t_form.user = request.user
            t_form.save()
        allRatings = Rating.objects.filter(movie_id=movie_pk)
        # print(allRatings.values())

        print(type(list(allRatings.values())))
        # print(type(movie.ratings_set.count()))
        context = {'count': movie.ratings_set.count(), 'allRatings': list(allRatings.values()), }
        return JsonResponse(context)
    else:
        return HttpResponseBadRequest
    
@login_required
def selectMovie(request, genreId):
    if request.is_ajax():
        movies = Movie.objects.filter(genres=genreId)
        if len(movies) > 4:
            random_nums = random.sample(range(0, len(movies)-1), 4)
            movies = [movies[num] for num in random_nums]
        print(movies)
        # context = {'random_movies': movies}
        parse_movies = serializers.serialize('json', movies)
        return HttpResponse(parse_movies, content_type="text/json-comment-filtered")
    else:
        return HttpResponseBadRequest 

        