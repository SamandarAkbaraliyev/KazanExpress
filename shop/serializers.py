from rest_framework import serializers
from shop import models


class ShopListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Shop
        fields = (
            'id',
            'title',
            'description',
            'image',
        )
        extra_kwargs = {'image': {'required': False}, 'id': {'required': True}}





class CategoryListSerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = models.Category
        fields = (
            'id',
            'title',
            'description',
            'parent',
            'children',
        )

    def get_children(self, obj):
        children = obj.children.all()
        serializer = self.__class__(children, many=True)
        return serializer.data


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    parent = CategoryListSerializer()
    children = CategoryListSerializer(many=True)

    class Meta:
        model = models.Category
        fields = (
            'id',
            'title',
            'description',
            'parent',
            'children',
        )


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = (
            'id',
            'title',
            'description',
            'parent',
        )
        extra_kwargs = {'parent': {'required': False}}


class ProductListSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = (
            'id',
            'title',
            'description',
            'amount',
            'price',
            'is_active',
            'shop',
            'category',
        )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = ('image',)


class ProductUpdateSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = models.Product
        fields = (
            'id',
            'title',
            'description',
            'amount',
            'price',
            'is_active',
            'shop',
            'category',
            'images',
        )

    # def update(self, instance, validated_data):
    #     # Update product fields
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.amount = validated_data.get('amount', instance.amount)
    #     instance.price = validated_data.get('price', instance.price)
    #     instance.is_active = validated_data.get('is_active', instance.is_active)
    #     instance.shop = validated_data.get('shop', instance.shop)
    #     instance.category = validated_data.get('category', instance.category)
    #
    #     images_data = validated_data.get('images', [])
    #     for image_data in images_data:
    #         instance.images.create(image=image_data)
    #
    #     instance.save()
    #
    #     return instance

    def update(self, instnce, validated_data):
        images = validated_data.pop('images')
        updated_instance = super().update(instnce, validated_data)

        images_list = [models.Images(product=updated_instance, image=image) for image in images]
        models.Images.objects.bulk_create(*images_list)
        return updated_instance
