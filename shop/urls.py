from django.urls import path
from shop import views

urlpatterns = [

    path('shop/list/', views.ShopListAPIView.as_view()),
    path('shop/<int:pk>/update/', views.ShopRetrieveUpdateView.as_view()),

    path('category/list/', views.CategoryListAPIView.as_view()),
    path('category/<int:pk>/', views.CategoryRetrieveAPIView.as_view()),
    path('category/<int:pk>/update/', views.CategoryUpdateAPIView.as_view()),

    path('product/list/', views.ProductListAPIView.as_view()),
    path('product/<int:pk>/update/', views.ProductUpdateAPIView.as_view()),
    path('product/', views.ProductCreateAPIView.as_view()),
]
