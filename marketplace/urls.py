from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views



urlpatterns=[
    path('shop/',views.shop,name='shop'),
    path('product_detail/<slug:slug_cat>/<slug:slug_sub>/<slug:slug_prod>',views.product_details,name='product_detail'),
    path('products_by_category/<slug:slug>',views.shop,name='products_by_category'),
    path('products_by_subcategory/<slug:slug>/<slug:sub_slug>',views.shop,name='products_by_subcategory'),
    path('search/',views.search,name='search'),
    path('userprofile_view/<int:pk>/',views.user_profil_detail,name='user_profil_detail'),
    path('catalogue_recommended_product/',views.catalogue_recommended_product,name='catalogue_recommended_product'),
    path('catalogue_resquest_buy/',views.catalogue_resquest_buy,name='catalogue_resquest_buy'),
    path('catalogue/',views.catalogue,name='catalogue'),
]