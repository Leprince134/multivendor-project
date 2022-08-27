from django.contrib import admin
from .models import *

# Register your models here.

# Afficher les autres image de produits

class Product_Images(admin.TabularInline):
    model = Product_Image


class Additional_Informations(admin.TabularInline):
    model = Additional_Information


class ProductAttributes(admin.TabularInline):
    model = ProductAttribute

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images, Additional_Informations, ProductAttributes)
    list_display = ('product_name', 'price', 'category', 'section', 'Tags', 'total_quantity', 'Discount', 'featured_image', 'Availability')
    list_editable = ('Discount', 'category', 'featured_image', 'price', 'section', 'total_quantity', 'Availability')



admin.site.register(Section)
admin.site.register(Product, Product_Admin)
admin.site.register(Product_Image)
admin.site.register(Additional_Information)
admin.site.register(ProductAttribute)



admin.site.register(Slider)

admin.site.register(Banner_area)

admin.site.register(Main_Category)

admin.site.register(Category)

admin.site.register(Sub_Category)


