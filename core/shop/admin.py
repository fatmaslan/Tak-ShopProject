from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Category,ProductImage,Product,Brand,Carousal,CarousalImage,CategoryImage

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )



class CategoryImagesInline(admin.TabularInline):
    model=CategoryImage
    extra=3 


class CategoryAdmin(admin.ModelAdmin):
     list_display = ('id', 'name')
     search_fields = ('name',)
     list_filter = ('name',)
     inlines = [CategoryImagesInline]
    

 

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
     list_display = ('id', 'name')
     search_fields = ('name',)
     list_filter = ('name',)
     
class ProductImagesInline(admin.TabularInline):
    model=ProductImage
    extra=3    

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'get_categories') 
    list_filter = ('categories',)
    inlines = [ProductImagesInline]

    def get_categories(self,obj):
       return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description="categories"

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

class CarouselImageAdmin(admin.TabularInline):
    model = CarousalImage
    extra = 3

class CarousalAdmin(admin.ModelAdmin):
    inlines = [CarouselImageAdmin]

admin.site.register(Carousal, CarousalAdmin)