from django.test import SimpleTestCase

from users.indexing.index_core import build_primary_index
from users.indexing.records import ItemRecord
from users.indexing.search_engines import SearchFilters, indexed_search, sequential_search


def sample_records():
    return [
        ItemRecord(1, "found", "1", "1", "Relógio", "", "01010001", "2026-01-01"),
        ItemRecord(2, "found", "1", "1", "Celular", "", "01010003", "2026-01-03"),
        ItemRecord(3, "found", "1", "1", "Caderno", "", "01010002", "2026-01-02"),
        ItemRecord(4, "lost", "2", "2", "Documento", "", "02020001", "2026-01-04"),
    ]


class TestSearchEngines(SimpleTestCase):
    def test_sequential_search_filters_by_name(self):
        records = sample_records()
        result = sequential_search(records, SearchFilters(name_contains="Reló"))
        assert len(result) == 1
        assert result[0].item_id == 1

    def test_indexed_search_by_barcode(self):
        records = sample_records()
        index = build_primary_index(records, order_by="barcode")

        result = indexed_search(
            index,
            SearchFilters(
                status="found",
                category="1",
                location="1",
                barcode="01010002",
            ),
        )

        assert len(result) == 1
        assert result[0].item_id == 3

    def test_indexed_search_returns_empty_without_full_composite_key(self):
        records = sample_records()
        index = build_primary_index(records, order_by="barcode")

        result = indexed_search(
            index,
            SearchFilters(
                status="found",
                location="1",
                barcode="01010002",
            ),
        )

        assert result == []
