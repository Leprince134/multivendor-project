
from django.db import models
from django.utils.html import mark_safe
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Create your models here.

# Slider
class Slider(models.Model):
    DISCOUNT_DEAL = (
        ('HOT DEALS','HOT DEALS'),
        ('New Arraivels', 'New Arraivels'),
    )
    Image = models.ImageField(upload_to='media/slider_imgs')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL, max_length=255)
    SALE = models.IntegerField()
    Brand_Name = models.CharField(max_length=255)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=255)


    def __str__(self):
        return self.Brand_Name

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

# Banner_area
class Banner_area(models.Model):
    image = models.ImageField(upload_to='media/banner_img')
    Discount_Deal = models.CharField(max_length=255)
    Quote = models.CharField(max_length=255)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=255, null=True)


    def __str__(self):
        return self.Quote

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

# Main_Category
class Main_Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 


# Category
class Category(models.Model):
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name + " - " + self.main_category.name


# Sub_Category
class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.category.main_category.name + " - " + self.category.name + " - "  + self.name

# Creation des sections
class Section(models.Model):
    name = models.CharField(max_length=255) 


    def __str__(self):
        return self.name

# Product
class Product(models.Model):
    total_quantity = models.IntegerField()
    Availability = models.IntegerField()
    featured_image = models.CharField(max_length=255)
    price = models.FloatField()
    product_name = models.CharField(max_length=255)
    Discount = models.IntegerField()
    Product_Information = RichTextField()
    model_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Tags = models.CharField(max_length=255)
    Description = RichTextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    slug = models.SlugField(default='', max_length=255, null=True, blank=True)


    def __str__(self):
        return self.product_name

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    
# Create an easy slug for you django Project   
    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("product_detail", kwargs={"slug": self.slug})

    class Meta:
        db_table = "app_Product"


def create_slug(instance, new_slug=None):
    slug = slugify(instance.product_name)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.all().filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug ="%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Product)


class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Image_url = models.CharField(max_length=255) 

    def __str__(self):
        return self.product.product_name 

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url)) 



class Additional_Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)

    def __str__(self):
        return self.product.product_name   


# Color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='4. Colors'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title

# Size
class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='5. Sizes'

    def __str__(self):
        return self.title


# Product Attribute
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = ' ProductAttributes'

    def __str__(self):
        return self.product.title
