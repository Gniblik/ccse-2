from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [

    path("", views.login_view, name = "login"),
    path("signup/", views.signup_view, name = "signup"),
    path("products/", views.products_view, name = "products"),
    path("basket/", views.basket_view, name = "basket"),
    path("checkout/", views.checkout_view, name = "checkout"),
    path("orders/", views.orders_view, name = "orders"),
    path('add_to_basket/<int:product_id>/', views.add_to_basket, name='add_to_basket'),
    path('remove-from-basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    path("logout/", views.logout_view, name="logout"),
    path('admin/', admin.site.urls),
    
]

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
