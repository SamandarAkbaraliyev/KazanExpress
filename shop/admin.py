from django.contrib import admin
from django.apps import apps
from shop.models import Product, Images, Shop

# all other models
models = apps.get_models()


class ImageInline(admin.StackedInline):
    model = Images
    extra = 1


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    search_fields = ("title",)

    def has_view_or_change_permission(self, request, *args):
        return request.user.role.filter(role='Shop admin').exists()

    def has_delete_permission(self, request, *args):
        return request.user.is_superuser

    def has_add_permission(self, request, *args):
        return request.user.is_superuser


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageInline,)

    list_display = ('id', 'title', 'amount', 'shop', 'category', 'price')
    list_display_links = ('id', 'title', 'amount', 'shop')
    list_filter = ('shop',)

    ordering = ('price',)

    # fields = (('title', 'description'), 'amount')

    autocomplete_fields = ("shop",)
    search_fields = ('title',)
    # search_help_text = "You can search by title: "

    list_select_related = ("shop", 'category')
    list_per_page = 100


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_product_admin = request.user.role.filter(role='Product admin').exists()
        disabled_fields = set()

        if not is_product_admin:
            disabled_fields |= {
                'price',
                'amount',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

    def has_add_permission(self, request):
        return request.user.role.filter(role='Product admin').exists()

    def has_view_or_change_permission(self, request, *args):
        return request.user.role.filter(role='Product admin').exists()

    def has_delete_permission(self, request, *args):
        return request.user.is_superuser



for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
