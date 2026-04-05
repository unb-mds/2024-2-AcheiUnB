from dataclasses import dataclass

from .index_core import (
    PrimarySequentialIndex,
    binary_search_block,
    build_composite_key,
)
from .records import ItemRecord


@dataclass(frozen=True)
class SearchFilters:
    status: str | None = None
    category: str | None = None
    location: str | None = None
    barcode: str | None = None
    found_lost_date: str | None = None
    name_contains: str | None = None


def _contains(haystack: str, needle: str | None) -> bool:
    if not needle:
        return True
    return needle.lower() in haystack.lower()


def _matches_filters(record: ItemRecord, filters: SearchFilters) -> bool:
    return all(
        (
            not filters.status or record.status.lower() == filters.status.lower(),
            not filters.category or record.category.lower() == filters.category.lower(),
            not filters.location or record.location.lower() == filters.location.lower(),
            not filters.barcode or record.barcode == filters.barcode,
            not filters.found_lost_date or record.found_lost_date == filters.found_lost_date,
            _contains(record.name, filters.name_contains),
        )
    )


def sequential_search(
    records: list[ItemRecord],
    filters: SearchFilters | None = None,
) -> list[ItemRecord]:
    active_filters = filters or SearchFilters()
    return [item for item in records if _matches_filters(item, active_filters)]


def indexed_search(
    index: PrimarySequentialIndex,
    filters: SearchFilters | None = None,
) -> list[ItemRecord]:
    active_filters = filters or SearchFilters()
    key = build_composite_key(
        active_filters.status,
        active_filters.category,
        active_filters.location,
    )

    if any(not part for part in key):
        return []

    block = index.blocks.get(key, [])
    if not block:
        return []

    if index.order_by == 'barcode' and active_filters.barcode:
        candidate_block = binary_search_block(
            block,
            active_filters.barcode,
            order_by='barcode',
        )
    elif index.order_by == 'found_lost_date' and active_filters.found_lost_date:
        candidate_block = binary_search_block(
            block,
            active_filters.found_lost_date,
            order_by='found_lost_date',
        )
    else:
        candidate_block = block

    return [item for item in candidate_block if _matches_filters(item, active_filters)]
