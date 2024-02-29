import datetime

from django.http import HttpResponseForbidden
from rest_framework.exceptions import PermissionDenied

from shop import models
from shop import serializers
from shop import permissions
from django.db.models import F
from rest_framework import filters
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.mixins import PermissionRequiredMixin
from rest_framework.parsers import MultiPartParser, FormParser
from shop.filters import PriceRangeFilter

from django_filters.rest_framework import DjangoFilterBackend

from shop.throttling import DynamicTimeRestrictedThrottle


class ShopListAPIView(generics.ListAPIView):
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopListUpdateSerializer
    permission_classes = (IsAuthenticated, permissions.IsShopAdmin)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)


class ShopRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopListUpdateSerializer
    permission_classes = (IsAuthenticated, permissions.IsShopAdmin)


class CategoryListAPIView(generics.ListAPIView):
    queryset = models.Category.objects.all().filter(parent=None).prefetch_related('children')
    serializer_class = serializers.CategoryListSerializer
    permission_classes = (IsAuthenticated, permissions.IsCategoryAdmin)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'product__id', 'parent__title')


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = models.Category.objects.all().select_related('parent').prefetch_related('children')
    serializer_class = serializers.CategoryRetrieveSerializer
    permission_classes = (IsAuthenticated, permissions.IsCategoryAdmin)


class CategoryUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryUpdateSerializer
    permission_classes = (IsAuthenticated, permissions.IsCategoryAdmin)


class ProductListAPIView(generics.ListAPIView):
    queryset = models.Product.objects.all().select_related('shop', 'category')
    serializer_class = serializers.ProductListSerializer
    permission_classes = (IsAuthenticated, permissions.IsProductAdmin)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, PriceRangeFilter]
    search_fields = ('title', 'id')

    ordering_fields = ('price',)
    filterset_fields = ('is_active',)


class ProductUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductUpdateSerializer
    permission_classes = (IsAuthenticated, permissions.IsProductAdmin)

    # def put(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #
    #         images_data = request.FILES.getlist('images')
    #         for image_data in images_data:
    #             image_instance, _ = models.Images.objects.get_or_create(product=instance, image=image_data)
    #
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCreateAPIView(PermissionRequiredMixin, generics.ListCreateAPIView):
    queryset = models.Product.objects.all().annotate(uploaded_images=F('images__image'))
    serializer_class = serializers.ProductSerializer

    permission_required = ("view_product", "add_product")

    parser_classes = (MultiPartParser, FormParser)

    def get_throttles(self):
        start_time = datetime.time(14, 0)
        end_time = datetime.time(20, 0)
        return [DynamicTimeRestrictedThrottle(start_time, end_time)]

    def get_queryset(self):
        start_time = settings.ACCESS_ALLOWED_START_TIME
        end_time = settings.ACCESS_ALLOWED_END_TIME
        now = datetime.datetime.now().time()

        if datetime.datetime.strptime(start_time, '%H:%M').time() <= now <= datetime.datetime.strptime(end_time,
                                                                                                       '%H%M').time():
            return super().get_queryset()
        else:
            raise PermissionDenied("Access denied outside of allowed time interval")

    def perform_create(self, serializer):
        start_time = settings.ACCESS_ALLOWED_START_TIME
        end_time = settings.ACCESS_ALLOWED_END_TIME
        now = datetime.datetime.now().time()

        if datetime.datetime.strptime(start_time, '%H:%M').time() <= now <= datetime.datetime.strptime(end_time,
                                                                                                       '%H%M').time():
            serializer.save()
        else:
            raise PermissionDenied("Access denied outside of allowed time interval")
