from modeltranslation.translator import translator, TranslationOptions
from .models import Shop, Product


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class ShopTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Product, ProductTranslationOptions)
translator.register(Shop, ShopTranslationOptions)
