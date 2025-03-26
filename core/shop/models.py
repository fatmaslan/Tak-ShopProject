from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=email, username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)



    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name
    
class CategoryImage(models.Model):
    categories = models.ForeignKey(Category,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category_images/')

class Brand(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=155)
    price = models.FloatField()
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    brands = models.ManyToManyField('Brand',related_name='products', max_length=155, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_discounted = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
    images = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image of {self.product.name}"




class Carousal(models.Model):
    title = models.CharField(max_length=155)

    def __str__(self):
        return self.title
    
class CarousalImage(models.Model):
    carousal = models.ForeignKey(Carousal,related_name='images',on_delete=models.CASCADE)
    images = models.ImageField(upload_to='carousal_images/')

    def __str__(self):
        return f"Image of {self.carousal.title}"

class Cart(models.Model):
    user = models.ForeignKey(CustomUser,related_name='cart',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    
class CartItem(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    cart = models.ForeignKey(Cart,related_name='cart_items',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.cart.user.username}"
    
class FavoriteProducts(models.Model):
    user = models.ForeignKey(CustomUser,related_name='favCart',on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    cart = models.ForeignKey(Cart,related_name='fav_cart',on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
       unique_together = ('user', 'product')
    