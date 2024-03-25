# from django.urls import path
# from . import views

# app_name = "main"
# urlpatterns = [
#     path('',views.home, name="home"),
#     path('details/<int:id>/',views.detail, name="detail"),
# ]


# from django.urls import path
# from . import views

# app_name = "accounts"
# urlpatterns = [
#     path('register/', views.register, name="register"),
#     path('login/', views.login_view, name='login'),
#     path("logout/", views.logout_user, name="logout")
# ]

from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('register/', views.register, name="register"),
    path("login/", views.login_user, name='login'),
    path("logout/", views.logout_user, name="logout"),
]
