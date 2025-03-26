from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView,ProductViewSet,ProductImageViewSet,CategoryViewSet,BrandViewSet,ProductDetaiLViewSet,CarousalViewSet,CarousalImageViewSet,CartDetailView,AllCartsView,AddToCartView,FavoriteProductsViewSet,AddToFavoriteView,CategoryImageViewSet
from . import views


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'images', ProductImageViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'categoriesImage',CategoryImageViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'products', ProductDetaiLViewSet, basename="product-detail")
router.register(r'carousals', CarousalViewSet)
router.register(r'carousalImages', CarousalImageViewSet, basename='carousal-images')
router.register(r'favorites', FavoriteProductsViewSet, basename='favorites')


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('carts/', AllCartsView.as_view(), name='all-carts'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/<int:cart_item_id>/remove/', views.remove_cart_item, name='remove_cart_item'),
    path('fav/add/', AddToFavoriteView.as_view(), name='add_to_fav'),
    path('', include(router.urls)),
]
urlpatterns += router.urls