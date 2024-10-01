import pytest

from src.tests.unit_tests.in_memory_repositories.in_memory_database import InMemoryProductRepository


@pytest.fixture
def product_rep_test():
    return InMemoryProductRepository()

