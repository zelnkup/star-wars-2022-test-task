from django.urls import path

from src.star_wars.views import (
    CharactersDetailView,
    CharactersListView,
    get_characters_csv,
)

urlpatterns = [
    path("generate/", get_characters_csv, name="generate-csv"),
    path("", CharactersListView.as_view(), name="index"),
    path("<int:pk>/", CharactersDetailView.as_view(), name="character-detail"),
]
