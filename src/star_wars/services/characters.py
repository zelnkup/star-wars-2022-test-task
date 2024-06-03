import uuid
from dataclasses import dataclass
from datetime import datetime

import petl as etl
from django.core.files.base import ContentFile
from petl import MemorySource

from src.star_wars.models import CollectionRequest

__all__ = "SaveCharactersToCSVService"


@dataclass
class NormalizeCharactersTableService:
    """
    Service for normalizing data from SW API to CSV file
    :transform datetime to %Y-%m-%d
    :remove redundant columns
    :replace homeworld link to name
    """

    table: etl.Table
    planets_map: dict

    def __call__(self) -> etl.Table:
        return self._normalize_table()

    def _normalize_table(self):
        self._rename_table()
        self._convert_table()
        self._cutout_table()
        self._substitute_homeworlds()
        return self.table

    def _substitute_homeworlds(self):
        self.table = etl.convert(
            self.table, "homeworld", lambda v: self.planets_map.get(v)
        )

    def _rename_table(self):
        self.table = etl.rename(self.table, "edited", "date")

    def _convert_table(self):
        self.table = etl.convert(
            self.table,
            "date",
            lambda v: datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
                "%Y-%m-%d"
            ),
        )

    def _cutout_table(self):
        self.table = etl.cutout(
            self.table, "films", "species", "vehicles", "starships", "created", "url"
        )


@dataclass
class SaveCharactersToCSVService:
    """
    Service for saving fetched characters to csv
    """

    characters: list
    planets_map: dict
    memory_source = MemorySource()
    normalizer = NormalizeCharactersTableService

    def __call__(self) -> CollectionRequest:
        self.table = self._generate_table()
        return self.create_collection()

    def _generate_table(self):
        table = etl.fromdicts(self.characters)
        table = self.normalizer(table, self.planets_map)()
        return etl.tocsv(table, source=self.memory_source)

    def get_file_name(self) -> str:
        return uuid.uuid4().hex + ".csv"

    def create_collection(self) -> CollectionRequest:
        content_file = ContentFile(
            self.memory_source.getvalue(), name=self.get_file_name()
        )
        return CollectionRequest.objects.create(file=content_file)
