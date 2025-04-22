from django.contrib import admin
from .models import Product, ProductImage, Category, ColorVariant, SizeVariant

admin.site.register(Category)
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','price']
    inlines = [ProductImageAdmin]

admin.site.register(ProductImage)

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name','price']
    model = ColorVariant

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name' , 'price']

    model = SizeVariant


admin.site.register(Product,ProductAdmin)