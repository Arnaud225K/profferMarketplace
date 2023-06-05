from django.shortcuts import render
from marketplace.models import Slider,Banner, Category_Banner, Product

def home(request):
    all_sliders = Slider.objects.all().order_by('-id')[0:3]
    banners_bloc_1 = Banner.objects.filter(category__name="banner_bloc_1", status=Banner.ACTIVE).order_by('-id')[0:3]
    banners_bloc_2 = Banner.objects.filter(category__name="banner_bloc_2", status=Banner.ACTIVE).order_by('-id')[0:2]
    all_product = Product.objects.all()

    recommended_product = Product.objects.filter(section__section_name="Рекомендации", status_for_product=Product.ACTIVE)
    request_buy_product = Product.objects.filter(section__section_name="Заявки", status_for_product=Product.ACTIVE)
    product_and_service = Product.objects.filter(section__section_name="Товары_и_Услуги", status_for_product=Product.ACTIVE)
    



    context = {
        'all_sliders':all_sliders,
        'banners_bloc_1':banners_bloc_1,
        'banners_bloc_2':banners_bloc_2,
        'recommended_product':recommended_product,
        'request_buy_product':request_buy_product,
        'product_and_service':product_and_service,
        'all_product':all_product,

    }
    return render(request,'proffer/home.html',context)
