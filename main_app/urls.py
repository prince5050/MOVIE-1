from django.urls import path, include
from .views import *

urlpatterns = [
    path('', view_movie, name='movie'),
    path('add-movie/', add_movie, name='add_movie'),
    path('edit-movie/<int:id>/', edit_movie),
    path('delete-movie/<int:id>/', delete_movie),
    path('search-movie/', search_movie),
]