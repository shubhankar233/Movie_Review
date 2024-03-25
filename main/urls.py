# from django.urls import path
# from . import views

# app_name = "main"
# urlpatterns = [
#     path('',views.home, name="home"),
#     path('details/<int:id>/',views.detail, name="detail"),
# ]


from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('', views.home, name="home"),  # URL pattern for the home page
    path('details/<int:id>/', views.detail, name="detail"),  # URL pattern for details page with ID parameter
    path('addmovies/', views.add_movies, name="add_movies"),
    path('editmovies/<int:id>/', views.edit_movies, name="edit_movies"),
    path('deletemovies/<int:id>/', views.delete_movies, name="delete_movie"),
    path('addreview/<int:id>/',views.add_review,name="add_review"),
    path("editreview/<int:movie_id>/<int:review_id>/",views.edit_review, name="edit_review"),
    path("deletereview/<int:movie_id>/<int:review_id>/",views.delete_review, name="delete_review")
]
