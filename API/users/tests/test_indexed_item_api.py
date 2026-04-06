from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

from users.models import Category, Color, Item, Location

User = get_user_model()


class TestIndexedItemAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

        self.category, _ = Category.objects.get_or_create(
            category_id="01",
            defaults={"name": "Acessórios"},
        )
        self.other_category, _ = Category.objects.get_or_create(
            category_id="02",
            defaults={"name": "Documentos"},
        )

        self.color, _ = Color.objects.get_or_create(
            color_id="01",
            defaults={"name": "Preto"},
        )
        self.other_color, _ = Color.objects.get_or_create(
            color_id="02",
            defaults={"name": "Branco"},
        )

        self.location, _ = Location.objects.get_or_create(
            location_id="01",
            defaults={"name": "Biblioteca"},
        )
        self.other_location, _ = Location.objects.get_or_create(
            location_id="02",
            defaults={"name": "ICC"},
        )

        self.item = Item.objects.create(
            user=self.user,
            name="Relógio",
            description="Relógio preto",
            category=self.category,
            color=self.color,
            location=self.location,
            status="found",
            found_lost_date=timezone.now() - timedelta(days=1),
        )

    def test_indexed_engine_search_by_barcode(self):
        response = self.client.get(
            f"/api/items/?engine=indexed&status=found&category={self.category.id}"
            f"&location={self.location.id}&barcode={self.item.barcode}"
        )

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == self.item.id

    def test_indexed_engine_preserves_existing_name_filters(self):
        Item.objects.create(
            user=self.user,
            name="Carteira",
            description="Carteira preta",
            category=self.category,
            color=self.color,
            location=self.location,
            status="found",
            found_lost_date=timezone.now(),
        )

        response = self.client.get(
            f"/api/items/?engine=indexed&status=found&category={self.category.id}"
            f"&location={self.location.id}&barcode={self.item.barcode}&category_name=Acessórios"
            "&color_name=Preto&search=Relógio"
        )

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == self.item.id
        assert response.data["results"][0]["name"] == "Relógio"

    def test_indexed_engine_preserves_ordering(self):
        older_item = Item.objects.create(
            user=self.user,
            name="Guarda-chuva",
            description="Guarda-chuva preto",
            category=self.category,
            color=self.color,
            location=self.location,
            status="found",
            found_lost_date=timezone.now() - timedelta(days=2),
        )

        newer_item = Item.objects.create(
            user=self.user,
            name="Mochila",
            description="Mochila preta",
            category=self.category,
            color=self.color,
            location=self.location,
            status="found",
            found_lost_date=timezone.now(),
        )

        Item.objects.filter(id=older_item.id).update(
            created_at=timezone.now() - timedelta(days=3)
        )
        Item.objects.filter(id=self.item.id).update(
            created_at=timezone.now() - timedelta(days=2)
        )
        Item.objects.filter(id=newer_item.id).update(
            created_at=timezone.now() - timedelta(days=1)
        )

        response = self.client.get(
            f"/api/items/?engine=indexed&status=found&category={self.category.id}"
            f"&location={self.location.id}&barcode={self.item.barcode}&ordering=created_at"
        )

        assert response.status_code == 200
        ids = [item["id"] for item in response.data["results"]]
        assert ids[:3] == [older_item.id, self.item.id, newer_item.id]

    def test_indexed_engine_preserves_pagination(self):
        for index in range(30):
            Item.objects.create(
                user=self.user,
                name=f"Item {index}",
                description="Mesmo bloco indexado",
                category=self.category,
                color=self.color,
                location=self.location,
                status="found",
                found_lost_date=timezone.now() + timedelta(minutes=index),
            )

        response = self.client.get(
            f"/api/items/?engine=indexed&status=found&category={self.category.id}"
            f"&location={self.location.id}&barcode={self.item.barcode}&page=2"
        )

        assert response.status_code == 200
        assert response.data["count"] == 31
        assert len(response.data["results"]) == 4
        assert response.data["previous"] is not None

    def test_engine_indexed_falls_back_to_legacy_search_when_key_is_incomplete(self):
        response = self.client.get(f"/api/items/?engine=indexed&barcode={self.item.barcode}")

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == self.item.id

    def test_indexed_engine_respects_found_items_route_status(self):
        Item.objects.create(
            user=self.user,
            name="Documento",
            description="Documento perdido",
            category=self.category,
            color=self.other_color,
            location=self.location,
            status="lost",
            found_lost_date=timezone.now(),
        )

        response = self.client.get(
            f"/api/items/found/?engine=indexed&category={self.category.id}"
            f"&location={self.location.id}&barcode={self.item.barcode}"
        )

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["status"] == "found"
