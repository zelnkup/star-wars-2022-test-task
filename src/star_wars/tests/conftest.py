import pytest
from django.core.files.uploadedfile import UploadedFile

from src.star_wars.tests.factories import HomeWorldFactory, TemporaryCSVFactory


@pytest.fixture
def homeworld_map_factory():
    return HomeWorldFactory()


@pytest.fixture
def correct_csv_file():
    """
    Correct CSV file used for comparing after normalization
    :return:
    """
    return UploadedFile(
        TemporaryCSVFactory(
            rows=[
                [
                    "name",
                    "height",
                    "mass",
                    "hair_color",
                    "skin_color",
                    "eye_color",
                    "birth_year",
                    "gender",
                    "homeworld",
                    "date",
                ],
                [
                    "Luke Skywalker",
                    "172",
                    "77",
                    "blond",
                    "fair",
                    "blue",
                    "19BBY",
                    "male",
                    "Tatooine",
                    "2014-12-20",
                ],
                [
                    "C-3PO",
                    "167",
                    "75",
                    "n/a",
                    "gold",
                    "yellow",
                    "112BBY",
                    "n/a",
                    "Tatooine",
                    "2014-12-20",
                ],
            ]
        )
    )
