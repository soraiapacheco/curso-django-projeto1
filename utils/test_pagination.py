from unittest import TestCase


def make_pagination_range(page_range, qty_pages, current_page):
    return [1, 2, 3, 4]


class PaginationTest(TestCase):

    def test_make_pagination_range_returns_a_pagination_range(self):
        # [1] 2 3 4 5 6 7 8 9 10
        # 1 [2] 3 4 5 6 7 8 9 10
        # 2 3 4 5 6 [7] 8 9 10 11
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )

        self.assertEqual([1, 2, 3, 4], pagination)
