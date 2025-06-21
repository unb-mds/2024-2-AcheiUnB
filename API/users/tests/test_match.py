import pytest
from unittest.mock import patch
from users.models import Item
from users.match import find_and_notify_matches
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db()
class TestFindAndNotifyMatchesLogic:
    @pytest.fixture()
    def item_lost(self):
        return Item.objects.create(name="Carteira", status="lost")

    @pytest.fixture()
    def item_found(self):
        return Item.objects.create(name="Carteira", status="found")

    def test_ct1_lost_with_match(db):
        user = User.objects.create_user(username="lost", email="lost@unb.br", password="123")
        item_lost = Item.objects.create(name="Carteira", status="lost", user=user)
        match_item = Item.objects.create(name="Chave", status="found", user=user)

        with patch("users.match.get_potential_matches", return_value=[match_item]), \
            patch("users.match.send_match_notification.delay") as mock_notify:
            find_and_notify_matches(item_lost)

        mock_notify.assert_called_once()

    @patch("users.match.get_potential_matches")
    @patch("users.match.send_match_notification.delay")
    def test_ct2_lost_without_match(self, mock_notify, mock_matches, item_lost):
        mock_matches.return_value = []
        find_and_notify_matches(item_lost)
        mock_notify.assert_not_called()

    @patch("users.match.get_potential_matches")
    @patch("users.match.send_match_notification.delay")
    def test_ct3_status_not_lost(self, mock_notify, mock_matches, item_found):
        mock_matches.return_value = []
        find_and_notify_matches(item_found)
        mock_notify.assert_not_called()

    def test_ct4_found_with_match(db):
        user = User.objects.create_user(username="found", email="found@unb.br", password="123")
        item_found = Item.objects.create(name="Carteira", status="found", user=user)
        lost_item = Item.objects.create(name="Caderno", status="lost", user=user)

        with patch("users.match.get_potential_matches", return_value=[lost_item]), \
            patch("users.match.send_match_notification.delay") as mock_notify:
            find_and_notify_matches(item_found)

        mock_notify.assert_called_once()

    @patch("users.match.get_potential_matches")
    @patch("users.match.send_match_notification.delay")
    def test_ct5_found_without_match(self, mock_notify, mock_matches, item_found):
        mock_matches.return_value = []
        find_and_notify_matches(item_found)
        mock_notify.assert_not_called()

    @patch("users.match.get_potential_matches")
    @patch("users.match.send_match_notification.delay")
    def test_ct6_status_not_found(self, mock_notify, mock_matches):
        item = Item.objects.create(name="item estranho", status="devolvido")
        mock_matches.return_value = []
        find_and_notify_matches(item)
        mock_notify.assert_not_called()
