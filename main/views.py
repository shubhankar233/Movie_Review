from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *

from .models import Movie, Review
from .forms import ReviewForm
from django.db.models import Avg

# Create your views here.
def home(request):
    query = request.GET.get("title")
    allMovies = None
    if query:
        allMovies = Movie.objects.filter(name__icontains=query)
    else:
        allMovies = Movie.objects.all()

    
    context = {
        "movies": allMovies,
    }

    return render(request,'main/index.html', context)


#detail page

def detail(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=id).order_by("-comment")

    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average = round(average,2)
    context = {
        "movie": movie,
        "reviews": reviews,
        "average":average
    }
    return render(request, 'main/details.html', context)
    
# add movies to db
# def add_movies(request):
#     if request.method == "POST":
#         form = MovieForm(request.POST or None)

#         # check if the form is valid
#         if form.is_valid():
#             data = form.save(commit=False)
#             data.save()
#             return redirect("main:home")
#         else:
#             form = MovieForm()
#         return render(request, 'main/addmovies.html',{"form": form})

def add_movies(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form = MovieForm(request.POST)  # Create form instance with POST data
                if form.is_valid():  # Check if the form is valid
                    form.save()  # Save the form data to the database
                    return redirect("main:home")  # Redirect to the home page
            else:
                form = MovieForm()  # Create a new empty form for GET requests

            # Render the addmovies.html template with the form
            return render(request, 'main/addmovies.html', {"form": form,"controller": "Add Movies"})

        # if not admin
        else:
            return redirect("main:home")
            
    return redirect("accounts:login")

# edit movie

def edit_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # movies linked with id
            movie = Movie.objects.get(id=id)
            
            # form check
            if request.method == "POST":
                form = MovieForm(request.POST or None, instance = movie)
                #check form validty
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:detail", id)
            else:
                form = MovieForm(instance=movie)
            return render(request, 'main/addmovies.html',{"form":form, "controller":"Edit Movies"})
     # if not admin
        else:
            return redirect("main:home")
            
    return redirect("accounts:login")


# delete movie

def delete_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            movie = Movie.objects.get(id=id)

            movie.delete()
            return redirect ("main:home")

        else:
            return redirect("main:home")
            
    return redirect("accounts:login")

# def add_review(request,id):
#     if request.user.is_authenticated:
#         movie = Movie.objects.get(id=id)
#         if request.method == "POST":
#             form = ReviewForm(request.POST or None)
#             if form.is_valid():
#                 data = form.save(commit=False)
#                 data.rating= request.POST["comment"]
#                 data.user = request.user
#                 data.movie = movie
#                 data.save()
#                 return redirect("main:detail",id)
#         else:
#             form = ReviewForm()
#         return render(request,'main/details.html',{"form":form})
#     else:
#         return redirect("accounts:login")



def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect("main:detail", id)
        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {"form": form, "movie": movie})
    else:
        return redirect("accounts:login")


def edit_review(request, movie_id,  review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id = movie_id)
        # review
        review = Review.objects.get(movie=movie, id=review_id)

        #check if the review was done by loged in user
        if request.user == review.user:
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Out of range. select Rating from 0 to 10 "
                        return render(request, "main/editreview.html", {"error":error, "form":form})
                    else:
                        data.save()
                        return redirect("main:detail", movie_id)
            else:
                form = ReviewForm(instance=review)
            return render(request,"main/editreview.html",{"form":form})
        else:
            return redirect("main:detail",movie_id)
    else:
        return redirect("accounts:login")

# delete review 
def delete_review(request, movie_id,  review_id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id = movie_id)
        # review
        review = Review.objects.get(movie=movie, id=review_id)

        #check if the review was done by loged in user
        if request.user == review.user:
            #grant permissioin
            review.delete()

        return redirect("main:detail",movie_id)
    else:
        return redirect("accounts:login")