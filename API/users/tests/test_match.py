import pytest
from unittest.mock import patch
from django.contrib.auth import get_user_model

from users.models import Item, Category, Location, Color, Brand
from users.match import find_and_notify_matches

User = get_user_model()


@pytest.mark.django_db
class TestFindAndNotifyMatchesMCDC:
    """Casos de teste derivados da análise MC/DC para find_and_notify_matches."""
    @pytest.fixture
    def user_lost(self):
        return User.objects.create_user(
            username="user_lost",
            email="lost@aluno.unb.br",
            password="password123",
        )
    @pytest.fixture
    def user_found(self):
        return User.objects.create_user(
            username="user_found",
            email="found@aluno.unb.br",
            password="password123",
        )
    @pytest.fixture
    def category(self):
        return Category.objects.create(name="Eletrônicos")
    @pytest.fixture
    def location(self):
        return Location.objects.create(name="FGA - Sala A1")
    @pytest.fixture
    def color(self):
        return Color.objects.create(name="Preto")
    @pytest.fixture
    def brand(self):
        return Brand.objects.create(name="Samsung")

    def test_ct01_item_lost_with_match(self, user_lost, user_found, category, location):
        """CT01: Item perdido (lost) com matches encontrados.
        Esperado: adiciona matches ao item, salva e notifica o dono do item perdido.
        """
        lost_item = Item.objects.create(
            user=user_lost,
            name="Celular Perdido",
            description="Samsung Galaxy",
            category=category,
            location=location,
            status="lost",
            barcode="1010101010",
        )
        found_item = Item.objects.create(
            user=user_found,
            name="Celular Encontrado",
            description="Samsung Galaxy",
            category=category,
            location=location,
            status="found",
            barcode="1010101010",
        )
        with patch("users.match.get_potential_matches", return_value=[found_item]), \
             patch("users.tasks.send_match_notification.delay") as mock_notify:
            find_and_notify_matches(lost_item, max_distance=2)

        assert found_item in lost_item.matches.all()
        mock_notify.assert_called_once()
        call_kwargs = mock_notify.call_args[1]
        assert call_kwargs["to_email"] == user_lost.email
        assert call_kwargs["item_name"] == lost_item.name

    @patch("users.match.get_potential_matches")
    @patch("users.tasks.send_match_notification.delay")
    def test_ct02_item_lost_without_match(self, mock_notify, mock_matches, user_lost, category, location):
        """CT02: Item perdido (lost) sem matches encontrados.
        Esperado: nenhuma notificação enviada, matches não alterados.
        """
        lost_item = Item.objects.create(
            user=user_lost,
            name="Carteira Perdida",
            description="Carteira preta",
            category=category,
            location=location,
            status="lost",
            barcode="2020202020",
        )

        mock_matches.return_value = []

        find_and_notify_matches(lost_item, max_distance=2)

        mock_matches.assert_called_once_with(
            lost_item, opposite_status="found", max_distance=2
        )
        assert lost_item.matches.count() == 0
        mock_notify.assert_not_called()

    @patch("users.match.get_potential_matches")
    @patch("users.tasks.send_match_notification.delay")
    def test_ct03_status_not_lost(self, mock_notify, mock_matches, user_lost, category, location):
        """CT03: Item com status diferente de "lost" (ex.: "archived").
        
        Esperado: bloco if não executado, passa para elif (ou nenhuma ação).
        """
        archived_item = Item.objects.create(
            user=user_lost,
            name="Item Arquivado",
            description="Não é perdido nem encontrado",
            category=category,
            location=location,
            status="archived",
            barcode="3030303030",
        )

        mock_matches.return_value = []

        find_and_notify_matches(archived_item, max_distance=2)

        mock_notify.assert_not_called()

    def test_ct04_item_found_with_match(self, user_lost, user_found, category, location):
        """CT04: Item encontrado (found) com potenciais losts encontrados.
        
        Esperado: para cada lost_item, adiciona found como match, salva e notifica dono do lost.
        """
        found_item = Item.objects.create(
            user=user_found,
            name="Mochila Encontrada",
            description="Mochila azul",
            category=category,
            location=location,
            status="found",
            barcode="4040404040",
        )

        lost_item = Item.objects.create(
            user=user_lost,
            name="Mochila Perdida",
            description="Mochila azul",
            category=category,
            location=location,
            status="lost",
            barcode="4040404040",
        )

        with patch("users.match.get_potential_matches", return_value=[lost_item]), \
             patch("users.tasks.send_match_notification.delay") as mock_notify:
            find_and_notify_matches(found_item, max_distance=2)

        assert found_item in lost_item.matches.all()
        mock_notify.assert_called_once()
        call_kwargs = mock_notify.call_args[1]
        assert call_kwargs["to_email"] == user_lost.email
        assert call_kwargs["item_name"] == lost_item.name

    @patch("users.match.get_potential_matches")
    @patch("users.tasks.send_match_notification.delay")
    def test_ct05_item_found_without_match(self, mock_notify, mock_matches, user_found, category, location):
        """CT05: Item encontrado (found) sem potenciais losts compatíveis.
        
        Esperado: nenhuma notificação enviada, matches não alterados.
        """
        found_item = Item.objects.create(
            user=user_found,
            name="Guarda-chuva Encontrado",
            description="Guarda-chuva vermelho",
            category=category,
            location=location,
            status="found",
            barcode="5050505050",
        )

        mock_matches.return_value = []

        find_and_notify_matches(found_item, max_distance=2)

        mock_matches.assert_called_once_with(
            found_item, opposite_status="lost", max_distance=2
        )
        mock_notify.assert_not_called()

    @patch("users.match.get_potential_matches")
    @patch("users.tasks.send_match_notification.delay")
    def test_ct06_status_not_found(self, mock_notify, mock_matches, user_found, category, location):
        """CT06: Item com status diferente de "found" (ex.: "archived").
        
        Esperado: nenhuma ação executada (fim da função sem entrar no elif).
        """
        archived_item = Item.objects.create(
            user=user_found,
            name="Item Arquivado 2",
            description="Não é perdido nem encontrado",
            category=category,
            location=location,
            status="archived",
            barcode="6060606060",
        )
        mock_matches.return_value = []
        find_and_notify_matches(archived_item, max_distance=2)
        mock_notify.assert_not_called()
