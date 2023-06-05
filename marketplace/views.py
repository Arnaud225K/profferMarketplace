from django.shortcuts import render, get_object_or_404
from django.http import Http404
from marketplace.models import Product
from category.models import Category, Subcategory

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from accounts.models import Account

from django.db.models import Max, Min

def product_details(request,slug_cat,slug_sub,slug_prod):
    show_detail_product = None
    #show_detail_product = Product.objects.get(slug=slug)

    try:
        show_detail_product = Product.objects.filter(status_for_product=Product.ACTIVE).get(category__slug=slug_cat,subcategory__slug=slug_sub,slug=slug_prod)
    except Exception as e:
        raise e

    context = {
        'show_detail_product':show_detail_product,
    }

    return render(request,'proffer/product_detail.html',context)


def shop(request,slug=None,sub_slug=None):
    categories = None
    shop_product = None
    product_count = 0

    product_sales = Product.objects.filter(section__section_name="Акция", status_for_product=Product.ACTIVE)

    min_price = Product.objects.filter(status_for_product=Product.ACTIVE).aggregate(Min('price'))
    max_price = Product.objects.filter(status_for_product=Product.ACTIVE).aggregate(Max('price'))
    #print(min_price)
    #print(max_price)
    
    FilterPrice = request.GET.get('FilterPrice')

    try:
        if sub_slug == None:
            categories = get_object_or_404(Category, slug=slug)
            shop_product = Product.objects.order_by('-created_date').filter(category__category_name=categories,status_for_product=Product.ACTIVE)
            paginator = Paginator(shop_product,12)
            page = request.GET.get('page')
            paged_product = paginator.get_page(page)
            product_count = shop_product.count()
            if FilterPrice:
                Int_FilterPrice = int(FilterPrice)
                shop_product = Product.objects.order_by('-created_date').filter(category__category_name=categories,status_for_product=Product.ACTIVE,price__lte = Int_FilterPrice)
                paginator = Paginator(shop_product,12)
                page = request.GET.get('page')
                paged_product = paginator.get_page(page)
                product_count = shop_product.count()
        else:
            shop_product = Product.objects.order_by('-created_date').filter(category__slug=slug,subcategory__slug=sub_slug,status_for_product=Product.ACTIVE)
            paginator = Paginator(shop_product,12)
            page = request.GET.get('page')
            paged_product = paginator.get_page(page)
            product_count = shop_product.count()
            if FilterPrice:
                Int_FilterPrice = int(FilterPrice)
                shop_product = Product.objects.order_by('-created_date').filter(category__slug=slug,subcategory__slug=sub_slug,status_for_product=Product.ACTIVE,price__lte = Int_FilterPrice)
                paginator = Paginator(shop_product,12)
                page = request.GET.get('page')
                paged_product = paginator.get_page(page)
                product_count = shop_product.count()

    except Exception as e:
        raise e

    context = {
        'categories':categories,
        'shop_product':paged_product,
        'product_count':product_count,
        'product_sales':product_sales,
        'min_price':min_price,
        'max_price':max_price,
		'FilterPrice':FilterPrice,
    }

    return render(request,'proffer/shop/shop.html',context)

def catalogue_recommended_product(request):
    product_sales = Product.objects.filter(section__section_name="Акция", status_for_product=Product.ACTIVE)
    min_price = Product.objects.filter(status_for_product=Product.ACTIVE,section__section_name="Рекомендации").aggregate(Min('price'))
    max_price = Product.objects.filter(status_for_product=Product.ACTIVE,section__section_name="Рекомендации").aggregate(Max('price'))
    #print(min_price)
    #print(max_price)
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        shop_product = Product.objects.filter(status_for_product=Product.ACTIVE, section__section_name="Рекомендации", price__lte = Int_FilterPrice).order_by('-created_date')
    else:
        shop_product = Product.objects.filter(status_for_product=Product.ACTIVE, section__section_name="Рекомендации").order_by('-created_date')

    context = {
        'min_price':min_price,
        'max_price':max_price,
		'FilterPrice':FilterPrice,
        'product_sales':product_sales,
        'shop_product':shop_product,
    }
    return render(request,'proffer/shop/shop.html',context)

def catalogue_resquest_buy(request):

    product_sales = Product.objects.filter(section__section_name="Акция", status_for_product=Product.ACTIVE)

    min_price = Product.objects.filter(status_for_product=Product.ACTIVE,section__section_name="Заявки").aggregate(Min('price'))
    max_price = Product.objects.filter(status_for_product=Product.ACTIVE,section__section_name="Заявки").aggregate(Max('price'))
    #print(min_price)
    #print(max_price)
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        shop_product = Product.objects.filter(status_for_product=Product.ACTIVE, section__section_name="Заявки", price__lte = Int_FilterPrice).order_by('-created_date')
    else:
        shop_product = Product.objects.filter(status_for_product=Product.ACTIVE, section__section_name="Заявки").order_by('-created_date')    
    
    context = {
        'min_price':min_price,
        'max_price':max_price,
		'FilterPrice':FilterPrice,
        'shop_product':shop_product,
        'product_sales':product_sales,
    }
    return render(request,'proffer/shop/shop.html',context)

def catalogue(request):

    product_sales = Product.objects.filter(section__section_name="Акция", status_for_product=Product.ACTIVE)

    min_price = Product.objects.filter(status_for_product=Product.ACTIVE,section__section_name="Товары_и_Услуги").aggregate(Min('price'))
    max_price = Product.objects.filter(status_for_product=Product.ACTIVE,section__section_name="Товары_и_Услуги").aggregate(Max('price'))
    #print(min_price)
    #print(max_price)
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        shop_product = Product.objects.filter(status_for_product=Product.ACTIVE, section__section_name="Товары_и_Услуги", price__lte = Int_FilterPrice).order_by('-created_date')
    else:
        shop_product = Product.objects.filter(status_for_product=Product.ACTIVE, section__section_name="Товары_и_Услуги").order_by('-created_date')   
    context = {
        'min_price':min_price,
        'max_price':max_price,
		'FilterPrice':FilterPrice,
        'shop_product':shop_product,
        'product_sales':product_sales,
    }
    return render(request,'proffer/shop/shop.html',context)
    

def search(request):
    shop_product = None
    #product_count = 0

    product_sales = Product.objects.filter(section__section_name="Акция", status_for_product=Product.ACTIVE)

    min_price = Product.objects.filter(status_for_product=Product.ACTIVE).aggregate(Min('price'))
    max_price = Product.objects.filter(status_for_product=Product.ACTIVE).aggregate(Max('price'))
    #print(min_price)
    #print(max_price)
    
    FilterPrice = request.GET.get('FilterPrice')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            shop_product = Product.objects.order_by('-created_date').filter(status_for_product=Product.ACTIVE).filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(model_name__icontains=keyword) | Q(tags__icontains=keyword))
#            product_count = shop_product.count()
#            paginator = Paginator(shop_product,12)
#            page = request.GET.get('page')
#            paged_product = paginator.get_page(page)
#            product_count = shop_product.count()
            if FilterPrice:
                Int_FilterPrice = int(FilterPrice)
                shop_product = Product.objects.order_by('-created_date').filter(status_for_product=Product.ACTIVE).filter(price__lte = Int_FilterPrice)
            else:
                shop_product = Product.objects.order_by('-created_date').filter(status_for_product=Product.ACTIVE)



    context = {
        #'shop_product':paged_product,
        'shop_product':shop_product,
        #'product_count':product_count,
        'product_sales':product_sales,
        'min_price':min_price,
        'max_price':max_price,
	    'FilterPrice':FilterPrice,
    }

    return render(request,'proffer/shop/shop.html', context)



def user_profil_detail(request,pk=None):
    user = Account.objects.get(pk=pk)
    if not user.is_active:
        raise Http404()
    
    product_for_user = user.products.filter(status_for_product=Product.ACTIVE)

    product_sales = Product.objects.filter(section__section_name="Акция", status_for_product=Product.ACTIVE)

    context = {
        'user': user,
        'product_for_user':product_for_user,
        'product_sales':product_sales,
    }

    return render(request,'proffer/user_profil_detail.html',context)
