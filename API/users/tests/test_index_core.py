from django.test import SimpleTestCase

from users.indexing.index_core import (
    binary_search_block,
    build_composite_key,
    build_primary_index,
)
from users.indexing.records import ItemRecord


def sample_records():
    return [
        ItemRecord(1, "found", "1", "1", "a", "", "01010001", "2026-01-01"),
        ItemRecord(2, "found", "1", "1", "b", "", "01010003", "2026-01-03"),
        ItemRecord(3, "found", "1", "1", "c", "", "01010002", "2026-01-02"),
        ItemRecord(4, "lost", "2", "2", "d", "", "02020001", "2026-01-04"),
    ]


class TestIndexCore(SimpleTestCase):
    def test_build_composite_key_normalizes_values(self):
        assert build_composite_key(" Found ", " 1 ", " 1 ") == ("found", "1", "1")

    def test_build_primary_index_groups_and_sorts_by_barcode(self):
        index = build_primary_index(sample_records(), order_by="barcode")
        block = index.blocks[("found", "1", "1")]
        assert [item.barcode for item in block] == ["01010001", "01010002", "01010003"]

    def test_binary_search_block_finds_exact_barcode(self):
        index = build_primary_index(sample_records(), order_by="barcode")
        block = index.blocks[("found", "1", "1")]
        found = binary_search_block(block, "01010002", order_by="barcode")
        assert len(found) == 1
        assert found[0].item_id == 3
