from .index_core import (
    PrimarySequentialIndex,
    binary_search_block,
    build_composite_key,
)
from .records import ItemRecord


def _contains(haystack: str, needle: str | None) -> bool:
    if not needle:
        return True
    return needle.lower() in haystack.lower()


def _matches_filters(
    record: ItemRecord,
    status: str | None = None,
    category: str | None = None,
    location: str | None = None,
    barcode: str | None = None,
    found_lost_date: str | None = None,
    name_contains: str | None = None,
) -> bool:
    if status and record.status.lower() != status.lower():
        return False
    if category and record.category.lower() != category.lower():
        return False
    if location and record.location.lower() != location.lower():
        return False
    if barcode and record.barcode != barcode:
        return False
    if found_lost_date and record.found_lost_date != found_lost_date:
        return False
    if not _contains(record.name, name_contains):
        return False
    return True


def sequential_search(
    records: list[ItemRecord],
    *,
    status: str | None = None,
    category: str | None = None,
    location: str | None = None,
    barcode: str | None = None,
    found_lost_date: str | None = None,
    name_contains: str | None = None,
) -> list[ItemRecord]:
    return [
        item
        for item in records
        if _matches_filters(
            item,
            status=status,
            category=category,
            location=location,
            barcode=barcode,
            found_lost_date=found_lost_date,
            name_contains=name_contains,
        )
    ]


def indexed_search(
    index: PrimarySequentialIndex,
    *,
    status: str | None = None,
    category: str | None = None,
    location: str | None = None,
    barcode: str | None = None,
    found_lost_date: str | None = None,
    name_contains: str | None = None,
) -> list[ItemRecord]:
    key = build_composite_key(status, category, location)

    if any(not part for part in key):
        return []

    block = index.blocks.get(key, [])
    if not block:
        return []

    if index.order_by == "barcode" and barcode:
        candidate_block = binary_search_block(block, barcode, order_by="barcode")
    elif index.order_by == "found_lost_date" and found_lost_date:
        candidate_block = binary_search_block(
            block,
            found_lost_date,
            order_by="found_lost_date",
        )
    else:
        candidate_block = block

    return [
        item
        for item in candidate_block
        if _matches_filters(
            item,
            status=status,
            category=category,
            location=location,
            barcode=barcode,
            found_lost_date=found_lost_date,
            name_contains=name_contains,
        )
    ]
