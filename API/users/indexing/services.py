from .index_core import build_primary_index
from .records import item_to_record
from .search_engines import SearchFilters, indexed_search


def _split_search_terms(raw_search: str | None) -> list[str]:
    if not raw_search:
        return []
    return [term.lower() for term in raw_search.split() if term.strip()]


def _matches_search(item, terms: list[str]) -> bool:
    if not terms:
        return True

    searchable_fields = (
        item.name or "",
        item.description or "",
        getattr(item.category, "name", "") or "",
        getattr(item.location, "name", "") or "",
    )
    lowered_fields = tuple(field.lower() for field in searchable_fields)

    # Mirror DRF SearchFilter behavior: all terms must match at least one field.
    return all(any(term in field for field in lowered_fields) for term in terms)


def should_use_indexed_search(params, path: str) -> bool:
    status = params.get("status")
    if not status:
        if "items/found" in path:
            status = "found"
        elif "items/lost" in path:
            status = "lost"

    has_full_key = all(
        [
            status,
            params.get("category"),
            params.get("location"),
        ]
    )
    has_probe = bool(params.get("barcode") or params.get("found_lost_date"))

    return params.get("engine") == "indexed" and has_full_key and has_probe


def run_indexed_item_search(queryset, params, path: str):
    status = params.get("status")
    if not status:
        if "items/found" in path:
            status = "found"
        elif "items/lost" in path:
            status = "lost"

    filters = SearchFilters(
        status=status,
        category=str(params.get("category")) if params.get("category") is not None else None,
        location=str(params.get("location")) if params.get("location") is not None else None,
        barcode=params.get("barcode"),
        found_lost_date=params.get("found_lost_date"),
        name_contains=params.get("name_contains"),
    )

    items = list(
        queryset.select_related("category", "location", "color", "brand").prefetch_related(
            "images"
        )
    )

    records = [item_to_record(item) for item in items]

    order_by = "barcode" if filters.barcode else "found_lost_date"
    index = build_primary_index(records, order_by=order_by)

    matched_records = indexed_search(index, filters=filters)

    items_by_id = {item.id: item for item in items}
    matched_items = [
        items_by_id[record.item_id]
        for record in matched_records
        if record.item_id in items_by_id
    ]

    search_terms = _split_search_terms(params.get("search"))
    if not search_terms:
        return matched_items

    return [item for item in matched_items if _matches_search(item, search_terms)]
