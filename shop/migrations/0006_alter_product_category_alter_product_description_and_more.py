# Generated by Django 4.2.7 on 2024-02-27 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0005_product_main_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, related_name="product", to="shop.category"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="main_photo",
            field=models.ImageField(null=True, upload_to="product/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="shop",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="shop.shop"),
        ),
        migrations.AlterField(
            model_name="shop",
            name="image",
            field=models.ImageField(null=True, upload_to="shop/"),
        ),
    ]
