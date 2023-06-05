from typing import Any, Dict
from django import forms

from marketplace.models import Product,Image_product,Additional_information
from .models import Account, UserProfile
from .validators import allow_only_images_validator
from django.forms import BaseFormSet, BaseInlineFormSet, BaseModelFormSet

class RegistrationForm(forms.ModelForm):

    first_name = forms.CharField(max_length=50, required=True,widget=forms.TextInput(attrs={'id': 'firstname','autocomplete': 'off', 'placeholder':'введите имя...'}))
    last_name = forms.CharField(max_length=50, required=True,widget=forms.TextInput(attrs={'id': 'lastname','autocomplete': 'off', 'placeholder':'введите фамилию...'}))
    phone_number = forms.CharField(max_length=15, required=True,widget=forms.TextInput(attrs={'id': 'telephone','autocomplete': 'off','pattern':'[0-9]+','placeholder':'введите телефон','title':'только цифры'}))
    email = forms.EmailField(max_length=100, required=True,widget=forms.EmailInput(attrs={'id': 'email-id','autocomplete': 'off', 'placeholder':'введите почты'}))
    password = forms.CharField(max_length=100, required=True,widget=forms.PasswordInput(attrs={'id': 'password','autocomplete': 'off', 'placeholder':'введите пароль...'}))
    confirm_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'id': 'confirm_password','autocomplete': 'off', 'placeholder':'повторите пароль...'}))
    
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password',]


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Пароль не совпадает!"
            )

class UserForm(forms.ModelForm):
        class Meta:
          model = Account
          fields = ['first_name','last_name','phone_number',]
        
        def __init__(self, *args, **kwargs):
             super(UserForm, self).__init__(*args, **kwargs)
             for field in self.fields:
                  self.fields[field].widget.attrs['class'] = 'form-control'
             

class UserProfileForm(forms.ModelForm):
        #profile_picture = forms.ImageField(required=False, error_messages={'invalid':("Только файлы изображений")}, widget=forms.FileInput)
        profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False, validators=[allow_only_images_validator])
        class Meta:
          model = UserProfile
          fields = ['address_line','city','profile_picture',]

        def __init__(self, *args, **kwargs):
             super(UserProfileForm, self).__init__(*args, **kwargs)
             for field in self.fields:
                  self.fields[field].widget.attrs['class'] = 'form-control'



class ProductForm(forms.ModelForm):
    
    product_name = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={'class': 'form-control1','autocomplete': 'off', 'placeholder':'Например, Pneus 45'}))
    product_image = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=True, validators=[allow_only_images_validator])
    class Meta:
          model = Product
          fields = ['product_name','category','subcategory','status','price','discount','tags','district','address','product_image','model_name','description',]

    def __init__(self, *args, **kwargs):
          super(ProductForm, self).__init__(*args, **kwargs)
          for field in self.fields:
              self.fields[field].widget.attrs['class'] = 'form-control'



class ImageForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input','lang':'ru'}), required=True, validators=[allow_only_images_validator])
    class Meta:
          model = Image_product
          fields = ['image',]

class RequiredFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
                form.empty_permitted = False
                form.use_required_attribute = True            



#class AddInfoForm(forms.ModelForm):
#     class Meta:
#          model = Additional_information
##          fields = ['specification','detail',]