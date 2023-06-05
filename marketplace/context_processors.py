from chat.models import Messages
from .models import Wishlist, Product

def get_wishlist_counter(request):
    wishlist_count = 0
    if request.user.is_authenticated:
        try:
            wishlist_product = Wishlist.objects.filter(user=request.user)
            if wishlist_product:
                wishlist_count = wishlist_product.count()
            else:
                wishlist_count = 0
        except:
            wishlist_count = 0
    return dict(wishlist_count=wishlist_count)


def get_product_counter(request):
    product_counter = 0
    if request.user.is_authenticated:
        try:
            product_counter = Product.objects.filter(user=request.user,status_for_product=Product.ACTIVE)
            if product_counter:
                product_counter = product_counter.count()
            else:
                product_counter = 0
        except:
            product_counter = 0
    return dict(product_counter=product_counter)

def get_unread_msg_counter(request):
    unread_msg_counter = 0
    if request.user.is_authenticated:
        try:
            unread_msg_counter = Messages.objects.filter(reciepient=request.user, is_read=True)
            if unread_msg_counter:
                unread_msg_counter = unread_msg_counter.count()
            else:
                unread_msg_counter = 0
        except:
            unread_msg_counter = 0
    return dict(unread_msg_counter=unread_msg_counter)