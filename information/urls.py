from django.urls import path
from information.views import emp_views, boxing_views, delivery_views, filling_views, size_views, sheet_views, pay_type_views, order_type_views, product_views

app_name = "information"

urlpatterns = [
    # 카테고리
    path('category_mid_insert', product_views.category_mid_insert, name='category_mid_insert'),
    path('category_update', product_views.category_update, name='category_update'),
    path('category_delete', product_views.category_delete, name='category_delete'),
    # 제품
    path('product', product_views.product_view, name='product_view'),
    path('product_insert', product_views.product_insert, name='product_insert'),
    path('product_update', product_views.product_update, name='product_update'),
    path('product_delete', product_views.product_delete, name='product_delete'),
    # 사이즈
    path('size', size_views.size_view, name='size_view'),
    path('size_insert', size_views.size_insert, name='size_insert'),
    path('size_update', size_views.size_update, name='size_update'),
    path('size_delete', size_views.size_delete, name='size_delete'),
    # 시트
    path('sheet', sheet_views.sheet_view, name='sheet_view'),
    path('sheet_insert', sheet_views.sheet_insert, name='sheet_insert'),
    path('sheet_update', sheet_views.sheet_update, name='sheet_update'),
    path('sheet_delete', sheet_views.sheet_delete, name='sheet_delete'),
    # 필링
    path('filling', filling_views.filling_view, name='filling_view'),
    path('filling_get', filling_views.filling_get, name='filling_get'),
    path('filling_insert', filling_views.filling_insert, name='filling_insert'),
    path('filling_update', filling_views.filling_update, name='filling_update'),
    path('filling_delete', filling_views.filling_delete, name='filling_delete'),
    # 포장
    path('boxing', boxing_views.boxing_view, name='boxing_view'),
    path('boxing_get', boxing_views.boxing_get, name='boxing_get'),
    path('boxing_insert', boxing_views.boxing_insert, name='boxing_insert'),
    path('boxing_update', boxing_views.boxing_update, name='boxing_update'),
    path('boxing_delete', boxing_views.boxing_delete, name='boxing_delete'),
    # 주문경로
    path('order_type', order_type_views.order_type_view, name='order_type_view'),
    path('order_type_get', order_type_views.order_type_get, name='order_type_get'),
    path('order_type_insert', order_type_views.order_type_insert, name='order_type_insert'),
    path('order_type_update', order_type_views.order_type_update, name='order_type_update'),
    path('order_type_delete', order_type_views.order_type_delete, name='order_type_delete'),
    # 결제방법
    path('pay_type', pay_type_views.pay_type_view, name='pay_type_view'),
    path('pay_type_get', pay_type_views.pay_type_get, name='pay_type_get'),
    path('pay_type_insert', pay_type_views.pay_type_insert, name='pay_type_insert'),
    path('pay_type_update', pay_type_views.pay_type_update, name='pay_type_update'),
    path('pay_type_delete', pay_type_views.pay_type_delete, name='pay_type_delete'),
    # 배송방법
    path('delivery', delivery_views.delivery_view, name='delivery_view'),
    path('delivery_get', delivery_views.delivery_get, name='delivery_get'),
    path('delivery_insert', delivery_views.delivery_insert, name='delivery_insert'),
    path('delivery_update', delivery_views.delivery_update, name='delivery_update'),
    path('delivery_delete', delivery_views.delivery_delete, name='delivery_delete'),
    # 직원관리
    path('emp', emp_views.employee_view, name='emp_view'),
    path('emp_update', emp_views.emp_update, name='emp_update'),
    path('emp_delete', emp_views.emp_delete, name='emp_delete'),

]
