import pytest
from src.list_generator.categories.kpop import (
    fetch_names_kpop,
)


def test_fetch_names_kpop():
    number_of_persons = 10

    full_names = fetch_names_kpop(number_of_persons)

    assert (
        len(full_names) == number_of_persons
    ), f"Expected {number_of_persons}, but got {len(full_names)}"
    assert all(
        isinstance(name, str) for name in full_names
    ), "All names should be strings"
