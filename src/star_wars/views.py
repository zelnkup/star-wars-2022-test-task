import asyncio
from itertools import chain

import petl as etl
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from src.star_wars.models import CollectionRequest, HomeWorld
from src.star_wars.services.characters import SaveCharactersToCSVService
from src.star_wars.services.fetchers import GetCharactersService, GetPlanetsService
from src.star_wars.services.planets import GetPlanetsMap


def get_characters_csv(request):
    """
    View for generating csv file with characters
    If there is no planets in db, fetch them from SW API
    :param request:
    :return:
    """
    home_world = HomeWorld.objects.first()

    async def async_view():
        characters_results = await GetCharactersService().get_items()
        planets_results = home_world or await GetPlanetsService().get_items()
        return list(chain.from_iterable(characters_results)), planets_results

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        characters, planets = loop.run_until_complete(async_view())
    finally:
        loop.close()
    planets_map = GetPlanetsMap(planets)()
    instance = SaveCharactersToCSVService(characters, planets_map)()
    return HttpResponseRedirect(reverse("character-detail", args=[instance.pk]))


class CharactersListView(ListView):
    queryset = CollectionRequest.objects.order_by("-created_at")
    template_name = "characters.html"


class CharactersDetailView(DetailView):
    """
    View for displaying characters from csv file
    Layer for pagination and aggregation was placed in get_context_data
    For scalability, it is better to extract it to a separate layer like Filter in DRF
    """

    model = CollectionRequest
    template_name = "character.html"
    pagination_size = 10

    def get_context_data(self, **kwargs):
        # TODO: extract to filter/pagination layer
        context = super().get_context_data(**kwargs)
        instance = self.get_object()
        table = etl.fromcsv(instance.file.path)
        context["buttons"] = etl.header(table)
        if aggregation := self.request.GET.get("aggregation"):
            rows = aggregation.split(",")
            table = etl.aggregate(table, key=rows, aggregation=len)
            table = etl.skip(table, 1)  # skip header
            context["characters"] = table
            context["headers"] = rows + ["count"]
            return context
        context["headers"] = etl.header(table)
        size = self.request.GET.get("size") or self.pagination_size
        table = etl.skip(table, 1)  # skip header
        context["characters"] = etl.head(table, int(size) - 1)
        context["size"] = int(size) + self.pagination_size
        return context
