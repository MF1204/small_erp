from django.urls import path

from order_sheet.views import create_order, new_order, option_view, post_create

app_name = "sheet"

urlpatterns = [
    path('order_sheet', new_order, name='order_sheet'),
    path('option_view', option_view, name='option_view'),
    path('create_order', create_order, name='create_order'),
    path('post_create', post_create, name='post_create'),
]