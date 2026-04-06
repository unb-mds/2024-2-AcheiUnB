from dataclasses import dataclass

from users.models import Item


@dataclass(frozen=True)
class ItemRecord:
    item_id: int
    status: str
    category: str
    location: str
    name: str
    description: str
    barcode: str
    found_lost_date: str


def item_to_record(item: Item) -> ItemRecord:
    return ItemRecord(
        item_id=item.id,
        status=item.status or "",
        category=str(item.category_id or ""),
        location=str(item.location_id or ""),
        name=item.name or "",
        description=item.description or "",
        barcode=item.barcode or "",
        found_lost_date=(
            item.found_lost_date.date().isoformat() if item.found_lost_date else ""
        ),
    )
