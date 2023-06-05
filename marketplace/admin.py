from django.contrib import admin
from .models import Product, Section, Image_product, Additional_information, Slider, Category_Banner,Banner, Wishlist


# Register model ---slider---
class SliderAdmin(admin.ModelAdmin):
    list_display=('discount','title',)
    
admin.site.register(Slider,SliderAdmin)

# Register model ---Category_Banner---
class AdminCategory_Banner(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    
    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False
    
    def has_change_permission(self, request, obj=None):
        # Disable edit
        return False

    
admin.site.register(Category_Banner,AdminCategory_Banner)

# Register model ---banner_area---
class BannerAdmin(admin.ModelAdmin):
    list_display=('title','intro','category')
    
admin.site.register(Banner,BannerAdmin)

# Register model ---section---
# Register model ---Category_Banner---
class AdminSection(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        # Disable delete
        return False
    
    def has_change_permission(self, request, obj=None):
        # Disable edit
        return False
admin.site.register(Section,AdminSection)

class Product_imageAdmin(admin.TabularInline):
    model = Image_product

class Additional_InformationsAdmin(admin.TabularInline):
    model = Additional_information

class ProductAdmin(admin.ModelAdmin):
    inlines = (Product_imageAdmin,Additional_InformationsAdmin)
    list_display=('product_name','price','category','subcategory','modified_date','user')
    prepopulated_fields = {'slug':('product_name',)}
    search_fields = ('category__category_name','subcategory__subcategory_name','product_name','user__email')
    #list_filter = ('is_available',)
    #list_editable=('category','subcategory','section','is_available')
admin.site.register(Product,ProductAdmin)


# Register model ---product_image---
admin.site.register(Image_product)
# Register model ---additional_information---
admin.site.register(Additional_information)

# Register model ---Wishlist---
class WishlistAdmin(admin.ModelAdmin):
    list_display=('product','user',)

admin.site.register(Wishlist,WishlistAdmin)