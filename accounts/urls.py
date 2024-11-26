from django.urls import path
from .views import register_view, login_view,home,logout_view,add_product,product_list

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register_view, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-product/', add_product, name='add_product'),
    path('products/', product_list, name='product_list'),
]
