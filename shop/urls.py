from django.urls import path
from shop import views
from django.views.decorators.cache import cache_page

urlpatterns = [

    path('shop/list/', views.ShopListAPIView.as_view()),
    path('shop/<int:pk>/update/', views.ShopRetrieveUpdateView.as_view()),

    path('category/list/', cache_page(60*15)(views.CategoryListAPIView.as_view())),
    path('category/<int:pk>/', views.CategoryRetrieveAPIView.as_view()),
    path('category/<int:pk>/update/', views.CategoryUpdateAPIView.as_view()),

    path('product/list/', cache_page(60*15)(views.ProductListAPIView.as_view())),
    path('product/<int:pk>/update/', views.ProductUpdateAPIView.as_view()),
    path('product/', views.ProductCreateAPIView.as_view()),
]
