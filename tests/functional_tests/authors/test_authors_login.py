import pytest

from .base import AuthorBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorBaseTest):
    def test_the_test(self):
        assert 1 == 1
