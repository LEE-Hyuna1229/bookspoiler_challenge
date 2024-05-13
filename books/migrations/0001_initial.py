# Generated by Django 5.0.6 on 2024-05-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("author", models.CharField(blank=True, max_length=255, null=True)),
                ("published", models.CharField(blank=True, max_length=255, null=True)),
                ("book_img", models.URLField(blank=True, null=True)),
                ("coupang_link", models.URLField(blank=True, null=True)),
                ("is_exposed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]