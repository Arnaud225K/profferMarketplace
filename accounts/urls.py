from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('',views.dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>',views.activate, name='activate'),
    path('forgotPassword/',views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/',views.resetPassword, name='resetPassword'),

    path('edit_profile/',views.edit_profile, name='edit_profile'),
    path('user_product/',views.user_product, name='user_product'),
    path('product_builder/add/', views.add_product, name='add_product'),
    path('product_builder/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product_builder/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('user_wishlist/', views.user_wishlist, name='user_wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('delete_to_wishlist/<int:product_id>/', views.delete_to_wishlist, name='delete_to_wishlist'),
    path('user_message/', views.chat, name='user_message'),
    path('user_message_page/<str:username>', views.directs, name='user_message_page'),
    path('send/', views.sendDirect, name = "send-directs"),
    path('notification/', views.notification, name = "notification"),
]