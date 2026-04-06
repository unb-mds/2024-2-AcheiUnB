from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.test import TestCase

from users.models import (
    Item,
    ItemImage,
    UserProfile,
)
from users.signals import (
    save_user_profile,
)


class UserProfileSignalTests(TestCase):

    def test_create_user_profile_signal(self):
        user = User.objects.create_user(username="testuser", password="password")

        assert UserProfile.objects.filter(user=user).exists()
        assert user.profile is not None

    def test_save_user_profile_signal(self):
        user = User.objects.create_user(username="testuser2", password="password")
        user.profile.profile_picture = "http://example.com/image.jpg"
        user.profile.save()

        save_user_profile(User, user)
        user.refresh_from_db()

        assert user.profile.profile_picture == "http://example.com/image.jpg"


class WelcomeEmailSignalTests(TestCase):

    @patch("users.tasks.send_welcome_email.delay")
    def test_send_welcome_email_on_first_login(self, mock_send_email):
        user = User.objects.create_user(
            username="testuser3",
            password="password",
            email="testuser3@example.com",
        )

        user_logged_in.send(sender=User, request=None, user=user)

        mock_send_email.assert_called_once_with(user.email, user.username)

        user.profile.refresh_from_db()
        assert user.profile.welcome_email_sent

        user_logged_in.send(sender=User, request=None, user=user)
        mock_send_email.assert_called_once()


class CloudinarySignalTests(TestCase):

    @patch("cloudinary.uploader.destroy")
    def test_delete_image_from_cloudinary(self, mock_cloudinary_destroy):

        item = Item.objects.create(name="Chave", status="lost")

        image = ItemImage.objects.create(
            item=item, image_url="http://res.cloudinary.com/demo/image/upload/sample.jpg"
        )

        image.delete()

        mock_cloudinary_destroy.assert_called_once_with("sample")
