from django.contrib import admin
from django.urls import path

from Pokedex import views

urlpatterns = [
    path('pokedex/<str:id>', views.index, name='index'),
    path('admin/', admin.site.urls)
]