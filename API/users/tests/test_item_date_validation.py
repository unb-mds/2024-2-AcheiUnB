"""
Testes para validação de data/hora de itens perdidos e achados.
Garante que não seja possível registrar itens com datas/horas futuras.
"""

from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from users.models import Category, Item, Location
from users.serializers import ItemSerializer


class ItemDateValidationTest(APITestCase):
    """Testes de validação de data/hora em itens."""

    def setUp(self):
        """Configura dados iniciais para os testes."""
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.category, _ = Category.objects.get_or_create(
            category_id="99", defaults={"name": "Test Eletrônicos"}
        )
        self.location, _ = Location.objects.get_or_create(
            location_id="99", defaults={"name": "Test Biblioteca"}
        )

    def test_create_item_with_past_datetime_success(self):
        """Teste: Deve permitir criar item com data/hora no passado."""
        past_datetime = timezone.now() - timedelta(hours=2)

        data = {
            "name": "Notebook Dell",
            "description": "Notebook preto encontrado na biblioteca",
            "category": self.category.id,
            "location": self.location.id,
            "status": "found",
            "found_lost_date": past_datetime.isoformat(),
            "user": self.user.id,
        }

        serializer = ItemSerializer(data=data)
        assert serializer.is_valid()
        item = serializer.save(user=self.user)
        assert item.id is not None

    def test_create_item_with_current_datetime_success(self):
        """Teste: Deve permitir criar item com data/hora atual."""
        current_datetime = timezone.now()

        data = {
            "name": "Mochila Azul",
            "description": "Mochila encontrada agora",
            "category": self.category.id,
            "location": self.location.id,
            "status": "found",
            "found_lost_date": current_datetime.isoformat(),
            "user": self.user.id,
        }

        serializer = ItemSerializer(data=data)
        assert serializer.is_valid()

    def test_create_item_with_future_datetime_fails(self):
        """Teste: NÃO deve permitir criar item com data/hora no futuro."""
        future_datetime = timezone.now() + timedelta(hours=5)

        data = {
            "name": "Carteira",
            "description": "Carteira que será encontrada no futuro",
            "category": self.category.id,
            "location": self.location.id,
            "status": "lost",
            "found_lost_date": future_datetime.isoformat(),
            "user": self.user.id,
        }

        serializer = ItemSerializer(data=data)
        with pytest.raises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        assert "found_lost_date" in str(context.value)
        assert "futuro" in str(context.value).lower()

    def test_create_item_with_future_date_tomorrow_fails(self):
        """Teste: NÃO deve permitir criar item com data de amanhã."""
        tomorrow = timezone.now() + timedelta(days=1)

        data = {
            "name": "Celular",
            "description": "Celular encontrado amanhã",
            "category": self.category.id,
            "location": self.location.id,
            "status": "found",
            "found_lost_date": tomorrow.isoformat(),
            "user": self.user.id,
        }

        serializer = ItemSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_update_item_with_future_datetime_fails(self):
        """Teste: NÃO deve permitir atualizar item com data/hora futura."""
        past_datetime = timezone.now() - timedelta(hours=1)
        item = Item.objects.create(
            name="Chaves",
            user=self.user,
            category=self.category,
            location=self.location,
            status="lost",
            found_lost_date=past_datetime,
        )

        future_datetime = timezone.now() + timedelta(hours=3)
        data = {"found_lost_date": future_datetime.isoformat()}

        serializer = ItemSerializer(item, data=data, partial=True)
        with pytest.raises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        assert "found_lost_date" in str(context.value)

    def test_create_item_without_datetime_success(self):
        """Teste: Deve permitir criar item sem especificar data/hora."""
        data = {
            "name": "Guarda-chuva",
            "description": "Guarda-chuva vermelho",
            "category": self.category.id,
            "location": self.location.id,
            "status": "lost",
            "user": self.user.id,
        }

        serializer = ItemSerializer(data=data)
        assert serializer.is_valid()
        item = serializer.save(user=self.user)
        assert item.found_lost_date is None

    def test_create_item_with_future_datetime_one_minute_fails(self):
        """Teste: NÃO deve permitir item com horário 1 minuto no futuro."""
        future_datetime = timezone.now() + timedelta(minutes=1)

        data = {
            "name": "Óculos",
            "description": "Óculos de sol",
            "category": self.category.id,
            "location": self.location.id,
            "status": "found",
            "found_lost_date": future_datetime.isoformat(),
            "user": self.user.id,
        }

        serializer = ItemSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_backend_validation_message_in_portuguese(self):
        """Teste: Verifica se a mensagem de erro está em português."""
        future_datetime = timezone.now() + timedelta(hours=2)

        data = {
            "name": "Livro",
            "category": self.category.id,
            "location": self.location.id,
            "status": "found",
            "found_lost_date": future_datetime.isoformat(),
            "user": self.user.id,
        }

        serializer = ItemSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            error_message = str(e.detail["found_lost_date"][0])
            assert "futuro" in error_message.lower()
            assert "data" in error_message.lower()
