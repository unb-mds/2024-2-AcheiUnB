from django.contrib.auth.models import User
from django.db import models
from users.utils.validators import validate_date_not_too_old


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.URLField(null=True, blank=True)
    welcome_email_sent = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location_id = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color_id = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)
    brand_id = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    STATUS_CHOICES = [
        ("found", "Found"),
        ("lost", "Lost"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="lost")
    found_lost_date = models.DateTimeField(
        null=True, 
        blank=True, 
        validators=[validate_date_not_too_old]
        )
    created_at = models.DateTimeField(auto_now_add=True)

    barcode = models.CharField(max_length=10, editable=False, blank=True)
    matches = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="matched_with"
    )

    def save(self, *args, **kwargs):
        category_id = self.category.category_id if self.category else "00"
        location_id = self.location.location_id if self.location else "00"
        color_id = self.color.color_id if self.color else "00"
        brand_id = self.brand.brand_id if self.brand else "00"
        self.barcode = f"{category_id}{location_id}{color_id}{brand_id}"
        super().save(*args, **kwargs)

    def delete_with_related_chats(self):
        from chat.models import ChatRoom

        ChatRoom.objects.filter(item=self).delete()
        self.delete()

    def __str__(self):
        return f"{self.name} ({self.location})"


class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name="images", on_delete=models.CASCADE)
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.item.name}"
