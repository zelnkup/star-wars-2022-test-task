import csv
import tempfile

import factory

from src.star_wars.models import HomeWorld
from src.star_wars.tests.helpers import get_homeworld_map


class TemporaryFileFactory(factory.Factory):
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        tmp_file = kwargs["tmp_file"]
        tmp_file.seek(0)
        return tmp_file


class TemporaryCSVFactory(TemporaryFileFactory):
    class Meta:
        model = tempfile.NamedTemporaryFile

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        tmp_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w+")
        filewriter = csv.writer(tmp_file, delimiter=",")
        for row in kwargs.get("rows", []):
            filewriter.writerow(row)
        tmp_file.seek(0)
        return super()._create(model_class, tmp_file=tmp_file)


class HomeWorldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HomeWorld

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        obj.homeworld_map = get_homeworld_map()
        obj.save()
        return obj
