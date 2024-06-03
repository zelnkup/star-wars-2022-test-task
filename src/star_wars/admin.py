from django.contrib import admin

from src.star_wars.models import CollectionRequest, HomeWorld


@admin.register(CollectionRequest)
class CollectionRequestAdmin(admin.ModelAdmin):
    ...


@admin.register(HomeWorld)
class HomeWorldAdmin(admin.ModelAdmin):
    ...
