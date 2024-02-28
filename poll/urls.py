from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/', views.ProductView.as_view(), name='products'),
    path('basket/add/<int:product_id>/', views.BasketView.as_view(), name='basket_add'),
    path('basket/remove/<int:basket_id>', views.RemoveBasketView.as_view(), name='basket_remove'),
    path('product_list/', views.ProductListAndPaginateView.as_view(), name='product_list'),
    path('category/<int:category_id>', views.ProductListAndPaginateView.as_view(), name='category')
]