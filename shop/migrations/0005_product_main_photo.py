# Generated by Django 4.2.7 on 2024-02-26 10:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0004_remove_images_is_main_images_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="main_photo",
            field=models.ImageField(default=1, upload_to="product/"),
            preserve_default=False,
        ),
    ]
