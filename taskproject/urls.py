from django.contrib import admin
from django.urls import path
from authentication import views

urlpatterns = [
    path('users', views.userApis),
    path('users/<int:id>', views.userApis),
    path('userslogin', views.loginApi),
    path('fetchSingleStock', views.getStockDetail),
    path('searchStock', views.seacrhStock),
    path('addToWatchList', views.addToWatchList),
    path('deleteFromWatchList', views.addToWatchList),
    path('fetchWatchList', views.fetchWatchList),

    
]
