from rest_framework import serializers
from shop.models import CustomUser,Product,ProductImage,Category,Brand,Carousal,CarousalImage,Cart,CartItem,FavoriteProducts,CategoryImage


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
 
class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(source='images')  

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'product'] 

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        
class ProductDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'images', 'brands', 'categories']

class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,read_only=True,source="product")
    class Meta:
        model = Brand
        fields = ['id', 'name', 'products']

class CategoryImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()  

    class Meta:
        model = CategoryImage
        fields = ['image','id']
         
class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    images = CategoryImageSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'products','images']

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    images = CategoryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'products', 'image')
class CarousalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarousalImage
        fields = ['id', 'images', 'carousal']

class CarousalSerializer(serializers.ModelSerializer):
    images = CarousalImageSerializer(many=True, read_only=True)

    class Meta:
        model = Carousal
        fields = ['id', 'title', 'images']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.product and obj.product.images.exists():
           return obj.product.images.first().images.url  
        return None

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'cart', 'image']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True,source='cart_items',)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

class FavoriteProductsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = FavoriteProducts
        fields = '__all__'

