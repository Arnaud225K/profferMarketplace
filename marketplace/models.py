from django.db import models
from category.models import Category, Subcategory
from accounts.models import Account, UserProfile
from ckeditor.fields import RichTextField

from django.db.models.signals import pre_save # Signals
# import the unique_slug_generator from .utils.py 
from .utils import unique_slug_generator

STATUS_PRODUCT=[
    ('Продавать','Продавать'),
    ('Покупать','Покупать'),
]

# Model ----Slider-----
class Slider(models.Model):
    DISCOUNT_CHOICES = (
        ('ГОРЯЧИЕ ПРЕДЛОЖЕНИЯ','ГОРЯЧИЕ ПРЕДЛОЖЕНИЯ'),
        ('НОВЫЕ ПОСТУПЛЕНИЯ','НОВЫЕ ПОСТУПЛЕНИЯ'),
        ('НОВЫЕ ПРЕДЛОЖЕНИЯ','НОВЫЕ ПРЕДЛОЖЕНИЯ'),
    )
    discount=models.CharField(max_length=100,choices=DISCOUNT_CHOICES,default='ГОРЯЧИЕ ПРЕДЛОЖЕНИЯ')
    title = models.CharField(max_length=255,unique=True)
    intro = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/slider')
    link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Slider'
        verbose_name_plural = 'sliders'

    def __str__(self):
        return self.title

class Category_Banner(models.Model):
        name = models.CharField(max_length=255)
        slug = models.SlugField(unique=True, null=False)

        class Meta:
            verbose_name_plural = 'Category Banner'

        def __str__(self):
            return self.name

        def get_absolute_url(self):
            return self.slug

    
# Model ----banner_area-----
class Banner(models.Model):
    DRAFT = 'draft'
    ACTIVE = 'active'

    STATUS_BANNER = (
        (DRAFT, 'Draft'),
        (ACTIVE, 'Active'),
    )
    category = models.ForeignKey(Category_Banner, related_name="banners", on_delete=models.CASCADE)
    title = models.CharField(max_length=255,unique=True)
    intro = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/banner')
    link = models.CharField(max_length=255, null=True, blank=True)
    status= models.CharField(max_length=50, choices=STATUS_BANNER, default=ACTIVE)

    class Meta:
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'

    def __str__(self):
        return self.title

# Model ----Section-----
class Section(models.Model):
    section_name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'sections'

    def __str__(self):
        return self.section_name
    

# Model ----Product-----
class Product(models.Model):
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    INACTIVE = 'Inactive'

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (WAITING_APPROVAL, 'Waiting approval'),
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    )

    DISTRICT_CHOICES=(
        ('Верх-Исетский район','Верх-Исетский район'),
        ('Железнодорожный район','Железнодорожный район'),
        ('Кировский район','Кировский район'),
        ('Ленинский район','Ленинский район'),
        ('Лесное кладбище','Лесное кладбище'),
        ('Октябрьский район','Октябрьский район'),
        ('Орджоникидзевский район','Орджоникидзевский район'),
        ('Чкаловский район','Чкаловский район'),
        ('микрорайон ЖБИ','микрорайон ЖБИ'),
        #('территория Юго-Восточный Район Изоплит','территория Юго-Восточный Район Изоплит'),
    )

    user = models.ForeignKey(Account, related_name='products', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, unique=True)
    status=models.CharField(max_length=15,choices=STATUS_PRODUCT, default='Продавать')
    status_for_product = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)
    price = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    district = models.CharField(choices=DISTRICT_CHOICES, max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, unique=False, null=True, blank=True) 
    product_image = models.ImageField(upload_to='media/product', null=True, blank=True)
    #product_information = RichTextField(null=True, blank=True)
    #product_information = models.TextField(max_length=250, blank=True)
    model_name = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    #description = RichTextField(blank=True)
    description = models.TextField(max_length=250, null=True, blank=True)
    #is_available = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    #Foreignkey
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    section = models.ManyToManyField(Section, blank=True)
    #slug for link
    slug = models.SlugField(max_length=500, unique=True, blank=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'products'

    def clean(self):
        self.product_name = self.product_name.capitalize()

    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        from django.urls import reverse
        #return reverse("product_detail", kwargs={'slug': self.slug})
        return reverse('product_detail', args=[self.category.slug,self.subcategory.slug, self.slug])

def product_pre_save_receiver(sender, instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender=Product)
    

# Model ----Product_image-----
class Image_product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/product', blank=True, null=True)

    def __str__(self):
        return self.product.product_name + "_image"


# Model ----Additional_information-----
class Additional_information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=255, null=True, blank=True)
    detail = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.product.product_name + "_infosup"

# Model ----Wishlist-----
class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_name
