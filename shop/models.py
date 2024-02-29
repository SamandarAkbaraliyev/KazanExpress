from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def get_children(self):
        children = list()
        children.append(self)
        for child in self.children.all():
            children.extend(children.get_children())
        return children

    def __str__(self):
        return self.title


class Shop(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    image = models.ImageField(upload_to='shop/', null=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True)

    amount = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    is_active = models.BooleanField(default=True)
    main_photo = models.ImageField(upload_to='product/', null=True)

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product', null=True)

    def __str__(self):
        return self.title


class Images(models.Model):
    image = models.ImageField(upload_to='product/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    @classmethod
    def get_main_photo(cls, product_id):
        photo = Images.objects.filter(product_id=product_id).first()
        print(photo)
        if photo:
            return photo.image
        return None


@receiver(post_save, sender=Images)
def post_save__post_option(sender, instance, created, **kwargs):
    instance.product.main_photo = Images.get_main_photo(instance.product.id)
    instance.product.save()


__all__ = ['Category', 'Shop', 'Images']
