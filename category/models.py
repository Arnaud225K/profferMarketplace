from django.db import models
from django.urls import reverse

# Model ----Category-----
class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])


    def __str__(self):
        return self.category_name
    


# Model ----Subcategory-----
class Subcategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'subcategories'

    def get_url(self):
        return reverse('products_by_subcategory', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.subcategory_name
        #return self.category.category_name + ' --> ' + self.subcategory_name