from django.contrib import admin
from .models import Category, Subcategory


# Register model ---Category---
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display=('category_name','slug',)

admin.site.register(Category,CategoryAdmin)

# Register model ---Subcategory---
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('subcategory_name',)}
    list_display=('subcategory_name','category','slug',)

admin.site.register(Subcategory,SubcategoryAdmin)