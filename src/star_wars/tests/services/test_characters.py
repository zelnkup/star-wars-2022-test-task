import csv

import pytest

from src.star_wars.services.characters import SaveCharactersToCSVService
from src.star_wars.tests.helpers import get_homeworld_map, get_prepared_planets_for_csv


@pytest.mark.django_db
def test_save_characters_to_csv_ok(correct_csv_file):
    """
    Compare initial not normalized data fixture proceeded through normalizer with expected csv file
    """

    collection_request = SaveCharactersToCSVService(
        get_prepared_planets_for_csv(), get_homeworld_map()
    )()

    with collection_request.file.open("r") as file1:
        reader1 = csv.reader(file1.read())
        csv_data1 = list(reader1)

    with correct_csv_file.open("r") as file2:
        reader2 = csv.reader(file2.read())
        csv_data2 = list(reader2)

    assert csv_data1 == csv_data2
