from django.urls import path
from . import views

app_name='movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('genre_page/', views.genre_page, name='genre_page'),
    path('movie_detail/<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('rating_create/<int:movie_pk>/', views.rating_create, name='rating_create'),
    path('rating_delete/<int:movie_pk>/<int:rating_pk>/', views.rating_delete, name='rating_delete'),
    path('movie_modify/<int:movie_pk>/', views.movie_modify, name="movie_modify"),
    path('rating_modify/<int:movie_pk>/<int:rating_pk>/', views.rating_modify, name="rating_modify"),
    path('like/<int:movie_pk>/', views.like, name='like'),
    path('main/', views.main, name='main'),
    path('addRating/<int:movie_pk>/', views.addRating, name='addRating'),
    path('select/<int:genreId>/', views.selectMovie, name="select_Movie")

]
