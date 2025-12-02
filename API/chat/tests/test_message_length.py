import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture()
def authenticated_client(db):
    client = APIClient()
    user = User.objects.create_user(
        username="test_user", email="test@aluno.unb.br", password="testpass123"
    )
    client.force_authenticate(user=user)
    client.user = user
    return client


@pytest.fixture()
def created_message(authenticated_client):
    payload = {"content": "Mensagem teste"}
    response = authenticated_client.post("/api/chat/messages/", payload, format="json")
    assert response.status_code == 201
    return response.data


@pytest.mark.django_db()    
class TestMessageLengthValidation:

    @pytest.mark.parametrize(
        ("content", "expected_status", "test_id"),
        [
            ("a" * 79, 201, "CT02"),
            ("a" * 80, 201, "CT03"),
            ("a" * 81, 400, "CT01"),
            ("a" * 78 + "😀😀😀", 400, "CT04"),
            ("a" * 78 + "😀", 201, "CT05"),
            ("😀" * 85, 400, "CT06"),
            ("a" * 79 + " b", 400, "CT12"),
        ],
    )
    def test_post_message_boundary_and_emoji(
        self, authenticated_client, content, expected_status, test_id
    ):
        payload = {"content": content}
        response = authenticated_client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == expected_status, f"Falha no teste {test_id}"
        if expected_status == 400:
            assert "content" in response.data

    def test_post_message_composite_emoji(self, authenticated_client):
        emoji_familia = "👨‍👩‍👧‍👦"
        payload = {"content": emoji_familia * 15}
        response = authenticated_client.post("/api/chat/messages/", payload, format="json")

        assert response.status_code == 201, (
            f"Esperado 201 para 15 emojis visuais, "
            f"mas len() conta como {len(payload['content'])} code points"
        )

    @pytest.mark.parametrize(
        ("content", "expected_status"),
        [
            ("", 400),
            ("   ", 400),
        ],
    )
    def test_empty_message_rejected(self, authenticated_client, content, expected_status):
        payload = {"content": content}
        response = authenticated_client.post("/api/chat/messages/", payload, format="json")
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        ("update_content", "expected_status"),
        [
            ("x" * 81, 400),
            ("y" * 80, 200),
        ],
    )
    def test_patch_message_validation(
        self, authenticated_client, created_message, update_content, expected_status
    ):
        message_id = created_message["id"]
        update_payload = {"content": update_content}
        response = authenticated_client.patch(
            f"/api/chat/messages/{message_id}/", update_payload, format="json"
        )

        assert response.status_code == expected_status
        if expected_status == 400:
            assert "content" in response.data
        elif expected_status == 200:
            assert response.data["content"] == update_content

    @pytest.mark.parametrize(
        "content",
        [
            "z" * 81,
            "w" * 85,
        ],
    )
    def test_model_clean_validates_content_length(self, db, content):
        from chat.models import Message

        user = User.objects.create_user(
            username="test_model_user", email="model@aluno.unb.br", password="testpass123"
        )
        message = Message(sender=user, content=content)

        with pytest.raises(ValidationError) as exc_info:
            message.full_clean()

        assert "content" in str(exc_info.value)

    def test_emoji_with_skin_tone_modifiers(self, authenticated_client):
        emoji_with_modifier = "👋🏽"

        assert len(emoji_with_modifier) == 2, "Sanity check: emoji + modifier = 2 code points"

        payload = {"content": emoji_with_modifier * 80}
        response = authenticated_client.post("/api/chat/messages/", payload, format="json")
        assert response.status_code == 201, (
            f"Esperado 201 para 80 emojis com skin tone, "
            f"mas len() conta como {len(payload['content'])} code points"
        )

        payload_over = {"content": emoji_with_modifier * 81}
        response_over = authenticated_client.post(
            "/api/chat/messages/", payload_over, format="json"
        )
        assert response_over.status_code == 400, "Esperado 400 (excede limite)"
        assert "content" in response_over.data
