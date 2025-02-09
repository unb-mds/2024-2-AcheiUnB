# Generated by Django 5.1.4 on 2025-01-29 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_item_matches_alter_item_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="matches",
            field=models.ManyToManyField(
                blank=True, related_name="matched_with", to="users.item"
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="status",
            field=models.CharField(
                choices=[("found", "Found"), ("lost", "Lost")], default="lost", max_length=10
            ),
        ),
    ]
