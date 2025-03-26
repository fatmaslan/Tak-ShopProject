from django.db import models
from rest_framework import viewsets
from shop.models import Product,ProductImage,Brand,Category,Carousal,CarousalImage,Cart,CartItem,FavoriteProducts
from .serializers import RegisterSerializer,ProductSerializer,ProductImageSerializer,CategorySerializer,BrandSerializer,CarousalSerializer,CarousalImageSerializer,CategoryDetailSerializer,CartItemSerializer,CartSerializer,FavoriteProductsSerializer,CategoryImage,CategoryImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters
from rest_framework.decorators import action



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Bu işlem kullanıcıyı oluşturacak
            return Response({"message": "Kullanici başariyla oluşturuldu"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request , email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({"error": "Geçersiz kullanici adi veya şifre"}, status=status.HTTP_401_UNAUTHORIZED)
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', 'description']


    @action(detail=False, methods=['get'])
    def discounted(self, request):
        discounted_products = Product.objects.filter(is_discounted=True)
        serializer = self.get_serializer(discounted_products, many=True)
        return Response(serializer.data)

    def get(self,request,*args,**kwargs):
        product_id = kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            data = {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
                "description": product.description,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Ürün bulunamadi"}, status=status.HTTP_404_NOT_FOUND)
        
        
class ProductDetaiLViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductImageViewSet(viewsets.ModelViewSet):
   queryset= ProductImage.objects.all()
   serializer_class = ProductImageSerializer
   parser_classes=[MultiPartParser,FormParser]

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.prefetch_related('images').all()
    serializer_class = CategorySerializer

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class CategoryImageViewSet(viewsets.ModelViewSet):
   queryset= CarousalImage.objects.all()
   serializer_class = CategoryImageSerializer
   parser_classes=[MultiPartParser,FormParser]
    
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CarousalViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Carousal.objects.all()
    serializer_class = CarousalSerializer

    
class CarousalImageViewSet(viewsets.ModelViewSet):
    queryset = CarousalImage.objects.all()
    serializer_class = CarousalImageSerializer
    permission_classes = [permissions.AllowAny]

class CartDetailView(APIView):
    queryset = Cart.objects.all()
    permission_classes= [IsAuthenticated]

    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()  
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
class AddToCartView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.user
    
        if not user or not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        product_id = request.data.get("product_id")
        
        if not product_id:
            return Response({"error": "Product ID gereklidir."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Ürün bulunamadi."}, status=status.HTTP_404_NOT_FOUND)
        
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
        )
        if not created:
            cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
    

class AllCartsView(APIView):
    queryset = CartItem.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CartItemSerializer

    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"items": []})  # Boş sepet

        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
@api_view(['DELETE'])
def remove_cart_item(request, cart_item_id):  
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, id=cart_item_id)
        cart_item.delete()
        return Response({"message": "Ürün sepetten silindi."}, status=status.HTTP_204_NO_CONTENT)
    except CartItem.DoesNotExist:
        return Response({"error": "Sepette böyle bir ürün yok."}, status=status.HTTP_404_NOT_FOUND)
     
class FavoriteProductsViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteProductsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteProducts.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddToFavoriteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.user
    
        if not user or not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        product_id = request.data.get("product_id")
        
        if not product_id:
            return Response({"error": "Product ID gereklidir."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Ürün bulunamadi."}, status=status.HTTP_404_NOT_FOUND)
        
        favorite, created = FavoriteProducts.objects.get_or_create(
            user=user,
            product=product,
            )
        if not created:
            favorite.save()

        return Response(FavoriteProductsSerializer(favorite).data, status=status.HTTP_201_CREATED)
    