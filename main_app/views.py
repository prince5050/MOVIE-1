from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Movie


# Create your views here.
def view_movie(request):
    movie = Movie.objects.filter(status=1).order_by('id')

    page = request.GET.get('page', 1)
    paginator = Paginator(movie, 8)
    try:
        movie_obj = paginator.page(page)
    except PageNotAnInteger:
        movie_obj = paginator.page(1)
    except EmptyPage:
        movie_obj = paginator.page(paginator.num_pages)
    return render(request, 'movie-view.html', {'active': 'view', 'movie_obj': movie_obj})


def add_movie(request):
    if request.method == 'POST':
        if Movie.objects.filter(name=request.POST.get('name'), status='1'):
            messages.error(request, 'Movie name Already Exist! Try with another name')
            return redirect('add_movie')
        else:
            hotel_obj = Movie.objects.create(name=request.POST.get('name'),
                                             thumbnail=request.FILES.get('thumbnail'),
                                             director=request.POST.get('director'),
                                             actor=request.POST.get('actor'),
                                             writer=request.POST.get('writer'),
                                             release_date=request.POST.get('release_date'),
                                             )
            hotel_obj.save()
            messages.success(request, 'Movie has been Added Successfully')
            return redirect('movie')

    else:
        return render(request, 'add-movie.html', {'active': 'add'})


def edit_movie(request, id):
    movie_obj = Movie.objects.filter(pk=id, status='1')
    if movie_obj:
        if request.method == 'POST':
            Movie.objects.filter(pk=id, status='1').update(name=request.POST.get('name'),
                                                           director=request.POST.get('director'),
                                                           actor=request.POST.get('actor'),
                                                           writer=request.POST.get('writer'),
                                                           release_date=request.POST.get('release_date'),
                                                           )
            if request.FILES.get('thumbnail'):
                movie_obj = Movie.objects.get(pk=id)
                movie_obj.thumbnail = request.FILES.get('thumbnail')
                movie_obj.save()
            messages.success(request, 'Movie has been update Successfully')
            return redirect('movie')

        else:
            movie = Movie.objects.get(pk=id, status='1')
            return render(request, 'edit-movie.html', {'movie': movie})
    else:
        messages.error(request, "Movie doesn't Exist! ")
        return redirect('movie')


# Soft delete the Movie data
def delete_movie(request, id):
    movie_obj = Movie.objects.filter(pk=id)
    if movie_obj:
        Movie.objects.filter(pk=id).update(status='3')
        messages.success(request, 'Movie has been deleted Successfully')
        return redirect('movie')
    else:
        messages.error(request, "Movie doesn't Exist! ")
        return redirect('edit-movie/' + str(id) + '/')


def search_movie(request):
    movie_obj = Movie.objects.filter(
        Q(name__startswith=request.POST.get('keywords')) | Q(name__icontains=request.POST.get('keywords')), status='1')
    if movie_obj:
        html_code = ''
        for list_data in movie_obj:
            html_code += '<div class="col-md-3 col-sm-6">'
            html_code += '<div id="serv_hover"  class="room card mt-4">'
            html_code += ' <div class="room_img">'
            if list_data.thumbnail:
                html_code += '<figure><img src="' + list_data.thumbnail.url + '"alt="#"/></figure>'
            html_code += '</div>'
            html_code += '<div class="bed_room"><h3>' + list_data.name + '</h3></div>'
            html_code += '<div class="text-left p-2" style="min-height:190px;"><p><strong>Director :</strong>' + list_data.director + '</p><p' \
                                                                                                            '><strong' \
                                                                                                            '>Stars ' \
                                                                                                            ':</strong>' + list_data.actor + '</p><p><strong>Writer :</strong>' + list_data.writer + '</p><p><strong>Release date :</strong>' + list_data.release_date.strftime("%d/%m/%Y") + '</p> '
            html_code += '</div><div class="card-footer p-0"> <a href="/edit-movie/' + str(
                list_data.pk) + '/" class="col-12 ' \
                                'btn btn-warning" ' \
                                'style="border' \
                                '-radius:0px;"><b' \
                                '>Modify</b></a> '
            html_code += '</div></div></div>'
        return JsonResponse(data={
            'posts': html_code,
        })
    else:
        return JsonResponse(data={
            'posts': ' ',
        })
