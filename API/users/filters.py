import django_filters

from users.models import Item


class ItemFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category_id")
    location = django_filters.NumberFilter(field_name="location_id")
    barcode = django_filters.CharFilter(field_name="barcode", lookup_expr="exact")
    found_lost_date = django_filters.DateFilter(
        field_name="found_lost_date",
        lookup_expr="date",
    )
    name_contains = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    category_name = django_filters.CharFilter(
        field_name="category__name",
        lookup_expr="icontains",
    )
    location_name = django_filters.CharFilter(
        field_name="location__name",
        lookup_expr="icontains",
    )
    color_name = django_filters.CharFilter(field_name="color__name", lookup_expr="icontains")
    brand_name = django_filters.CharFilter(field_name="brand__name", lookup_expr="icontains")

    class Meta:
        model = Item
        fields = [
            "category",
            "location",
            "barcode",
            "found_lost_date",
            "name_contains",
            "category_name",
            "location_name",
            "color_name",
            "brand_name",
            "status",
        ]
