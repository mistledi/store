from operator import mod
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.



class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey('CardInfo', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_date = models.DateField(blank=True, null=True)
    tax = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    shipping_price = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    delivery_address = models.ForeignKey('ContactDetail', on_delete=models.CASCADE, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    order_status = models.CharField(max_length=1)
    quantity = models.BigIntegerField()

    
class OrderProduct(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('order', 'product'),)


    


class CardInfo(models.Model):
    card_number = models.BigIntegerField()
    expiry_date = models.DateField()
    cvv = models.IntegerField()
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_default = models.BooleanField(blank=True, null=True)

    




    
class ContactDetail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    address_id = models.BigIntegerField(primary_key=True)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    phone = models.CharField(max_length=20)
    is_default = models.BooleanField(blank=True, null=True)

    










class ProductShoppingcart(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE, primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)

    

class ProductWishlist(models.Model):
    product = models.OneToOneField('Product', on_delete=models.CASCADE, primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)

    


class WishList(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_added = models.DateField(blank=True, null=True)

    


class ShoppingCart(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_added = models.DateField(blank=True, null=True)

   



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Product(models.Model):
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    p_title = models.CharField(max_length=255, verbose_name="Title")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    p_price = models.DecimalField(max_digits=9, decimal_places=2)
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="URL")
    p_description = models.TextField(blank=True, verbose_name="Product description")
    p_photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Product photo')
    p_time_create = models.DateTimeField(auto_now_add=True)
    p_time_update = models.DateTimeField(auto_now=True)
    cat = models.ForeignKey('Category', on_delete = models.PROTECT)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    # mac, watch, iphone
    p_color =  models.CharField(max_length=255, verbose_name="Display")
    p_year = models.DateField(blank=True, null=True)
    p_capacity = models.IntegerField(blank=True, null=True, verbose_name="Capacity")
    p_display = models.CharField(blank=True, null=True, max_length=255, verbose_name="Display")
    p_model_processor = models.CharField(blank=True, null=True, max_length=255, verbose_name="Model Processor")
    p_weight = models.IntegerField(blank=True, null=True, verbose_name="Weight")
    p_charge = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    p_diogonal = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True),
    p_batery_capacity = models.DecimalField(decimal_places=2,max_digits = 10, blank=True, null=True)
    # watch and pencil
    p_type = models.CharField(blank=True, null=True, max_length=255, verbose_name="Type")
    p_fabric =  models.CharField(blank=True, null=True, max_length=255, verbose_name="Material")
    p_interfase = models.CharField(blank=True, null=True, max_length=255, verbose_name="Interface")
    
    
    
    count = models.IntegerField(blank=True, null=True, verbose_name="count")
    objects = models.Manager()
    published = PublishedManager()
    
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})
    




    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'post_slug': self.slug})

    # def get_absolute_url(self):
    #     return reverse('post', kwargs={"post_name": self.p_title})

    class Meta:
        ordering = ('-p_time_create',)

    def __str__(self):
        return self.p_title

    
    
class Category(models.Model):
    ct_category_name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="URL")



        
    def __str__(self):
        return self.ct_category_name
        
    
    def get_absolute_url(self):
        return reverse('category', kwargs={"cat_id": self.pk})



class Comment(models.Model):
    product = models.ForeignKey(Product,
                             on_delete=models.CASCADE,
                             related_name='comments',)
    # name = models.CharField(max_length=80)
    # email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'