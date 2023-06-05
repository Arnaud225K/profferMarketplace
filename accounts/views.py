import json
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify

from marketplace.context_processors import get_wishlist_counter
from chat.models import Messages

from .forms import ProductForm, RegistrationForm, UserForm, UserProfileForm, ImageForm, RequiredFormSet
from .models import Account, UserProfile
from marketplace.models import Product,Image_product, Wishlist
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.forms import FileInput, formset_factory, modelformset_factory

from .utils import get_user

#Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            phone_number = register_form.cleaned_data['phone_number']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #User ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Пожалуйста, активируйте ваш аккаунт'
            message = render_to_string('proffer/accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #messages.success(request, 'Регистрация прошла успешно!')
            #return redirect('register')
            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        register_form = RegistrationForm()

    context = {
        'register_form':register_form,
    }
    return render(request, 'proffer/accounts/register.html',context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Вы вошли в систему теперь!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверные данные для входа в систему!')
            return redirect('login')

    return render(request, 'proffer/accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, "Вы вышли из системы!")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Поздравляем! Ваш аккаунт успешно активирован.')
        return redirect('login')
    else:
        messages.error(request, 'Неверная ссылка активации!')
        return redirect('register')


@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'proffer/accounts/dashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #User PASSWORD RESET
            current_site = get_current_site(request)
            mail_subject = 'Сброс вашего пароля'
            message = render_to_string('proffer/accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'На ваш адрес электронной почты отправлено письмо о сбросе пароля.')
            return redirect('login')

        else:
            messages.error(request, 'Аккаунт не существует!')
            return redirect('forgotPassword')
    
    return render(request, 'proffer/accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Пожалуйста, сбросьте ваш пароль.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Срок действия данной ссылки истек!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Ваш пароль сброшен успешно!')
            return redirect('login')
        else:
            messages.error(request, 'Пароль не совпадает!')
            return redirect('resetPassword')
    else:
        return render(request, 'proffer/accounts/resetPassword.html')

@login_required(login_url = 'login')    
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile,
    }
    return render(request, 'proffer/accounts/edit_profile.html',context)


@login_required(login_url = 'login')  
def user_product(request):
    user = get_user(request)
    get_user_product = Product.objects.filter(user=user, status_for_product=Product.ACTIVE).order_by('created_date')
    get_user_product_waiting = Product.objects.filter(user=user, status_for_product=Product.WAITING_APPROVAL).order_by('created_date')
    get_user_product_inactive = Product.objects.filter(user=user, status_for_product=Product.INACTIVE).order_by('created_date')
    get_user_product_draft = Product.objects.filter(user=user, status_for_product=Product.DRAFT).order_by('created_date')
    context = {
        'get_user_product':get_user_product,
        'get_user_product_waiting':get_user_product_waiting,
        'get_user_product_inactive':get_user_product_inactive,
        'get_user_product_draft':get_user_product_draft,
    }
    return render(request, 'proffer/accounts/user_product.html',context)


@login_required(login_url = 'login')  
def add_product(request):                      
    #ImageFormset = modelformset_factory(Image_product, fields=('image',), extra=4, widgets={'image': FileInput(attrs={'class': 'custom-file-input','lang':'ru'})})
    ImageFormset = modelformset_factory(Image_product, extra=2, form=ImageForm, formset=RequiredFormSet)
    if request.method =='POST':
        form_product = ProductForm(request.POST,  request.FILES)
        image_formset = ImageFormset(request.POST, request.FILES)

        if form_product.is_valid() and image_formset.is_valid():
            product_name = form_product.cleaned_data['product_name']
            product = form_product.save(commit=False)
            product.user = get_user(request)
            #product.slug = ""
            form_product.save()

            if product.status == "Продавать":
                product.section.set([1,3])
            else:
                product.section.set([1,2])            

            for f in image_formset:
                try:
                    photo = Image_product(product=product, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break

            messages.success(request, 'Product added successful')
            return redirect('user_product')
        else:
            form_product.errors
            image_formset.errors
    else:
        form_product = ProductForm()
        image_formset = ImageFormset(queryset=Image_product.objects.none())

    context = {
        'form_product':form_product,
        'image_formset':image_formset,
    }
    return render(request, 'proffer/accounts/add_product.html',context)

@login_required(login_url = 'login')  
def edit_product(request, pk=None):

    product = get_object_or_404(Product, pk=pk)

    ImageFormset = modelformset_factory(Image_product, extra=2, form=ImageForm, formset=RequiredFormSet)

    if product.user != request.user:
        raise Http404()

    if request.method =='POST':
        form_product = ProductForm(request.POST,  request.FILES, instance=product)
        image_formset = ImageFormset(request.POST, request.FILES)

        if form_product.is_valid() and image_formset.is_valid():
            product_name = form_product.cleaned_data['product_name']
            product = form_product.save(commit=False)
            product.user = get_user(request)
            #product.slug = ""
            form_product.save()

            data = Image_product.objects.filter(product=product)
            for index, f in enumerate(image_formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = Image_product(product=product, image=f.cleaned_data['image'])
                        photo.save()
                    else:
                        photo = Image_product(product=product, image=f.cleaned_data['image'])
                        d = Image_product.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()

            messages.success(request, 'Product updated successful')
            return redirect('user_product')
        else:
            form_product.errors
    else:
        form_product = ProductForm(instance=product)
        image_formset = ImageFormset(queryset=Image_product.objects.filter(product=product))

    context = {
        'form_product':form_product,
        'product':product,
        'image_formset':image_formset,
    }
    return render(request, 'proffer/accounts/edit_product.html',context)


@login_required(login_url = 'login')  
def delete_product(request, pk=None):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status_for_product = Product.INACTIVE
    product.save()

    messages.success(request, 'Объявление успешно помечено как проданно!')

    return redirect('user_product')


@login_required(login_url = 'login')  
def user_wishlist(request):

    my_wishlist = Wishlist.objects.filter(user=request.user)
    
    context = {
        'my_wishlist':my_wishlist,
    }
    return render(request, 'proffer/accounts/user_wishlist.html',context)


def add_to_wishlist(request, product_id=None):
    if request.user.is_authenticated:
        if request.is_ajax():
            #check if the product is exits
            try:
                product = Product.objects.get(id=product_id)
                wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
                if wishlist_count > 0:
                    return JsonResponse({'status':'Failed', 'message':'Товар уже в избранных объявлениях!'})
                else:
                    new_wishlist = Wishlist.objects.create(user=request.user,product=product)
                    return JsonResponse({'status':'Success', 'message':'Товар добавлен в избранное!','wishlist_counter':get_wishlist_counter(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'Товар не существует!'})
        else:
            return JsonResponse({'status':'Failed', 'message':'Неверный запрос!'})
    else:
        return JsonResponse({'status':'Login_required', 'message':'Пожалуйста, авторизуйтесь, чтобы продолжить!'})


def delete_to_wishlist(request, product_id=None):
    if request.user.is_authenticated:
        if request.is_ajax():
            #check if the product is exits
            try:
                product = Product.objects.get(id=product_id)
                wishlist_check = Wishlist.objects.filter(product=product, user=request.user).get(product_id=product)
                wishlist_check.delete()
                return JsonResponse({'status':'Success', 'message':'Товар удален из избранных объявлений!','wishlist_counter':get_wishlist_counter(request)})                   
            except:
                return JsonResponse({'status':'Failed', 'message':'Товар не найден!'})
        else:
            return JsonResponse({'status':'Failed', 'message':'iНеверный запрос!'})
    else:
        return JsonResponse({'status':'Login_required', 'message':'Пожалуйста, авторизуйтесь, чтобы продолжить!'})
    

@login_required(login_url = 'login')  
def chat(request):
    user = request.user
    messages = Messages.get_message(user=user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Messages.objects.filter(user=request.user, reciepient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
    context = {
        'messages':messages,
        'directs':directs,
        'user':user,
        'active_direct':active_direct,
    }

    return render(request, 'proffer/accounts/user_message.html',context)

@login_required(login_url = 'login')  
def directs(request, username):
    user = request.user
    messages = Messages.get_message(user=user)
    active_direct = username
    directs = Messages.objects.filter(user=user, reciepient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    context = {
        'messages':messages,
        'directs':directs,
        'user':user,
        'active_direct':active_direct,
    }
    return render(request, 'proffer/accounts/user_message_page.html',context)


def sendDirect(request):
    if request.method == "POST":
        from_user = request.user
        to_user_username = request.POST['to_user']
        body = request.POST['body']

        try:
            to_user = Account.objects.get(username=to_user_username)
        except Exception as e:
            return redirect('home')
        
        if from_user != to_user:
            Messages.sender_message(from_user, to_user, body)

        success = "Message Sent"
        return HttpResponse(success)

@login_required(login_url = 'login')  
def notification(request):
    return render(request, 'proffer/accounts/user_notification.html')