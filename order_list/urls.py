from django.urls import path

from order_list.views import *

app_name = "list"

urlpatterns = [
    path('', order_list_view, name='home'),
    path('list/option_view', option_view, name='option_view'),
    path('list/page_list/', page_list.as_view(), name='page_list'),
    path('list/crud', crud, name='crud'),
    path('list/update', update, name='update'),
    path('list/delete', delete, name='delete'),
    path('list/printlist', printlist, name='printlist'),
    path('list/printall', printall, name='printall'),
    path('list/popup/', popup, name='popup'),
    path('list/changestatus', changestatus, name='changestatus'),
    path('list/autocomplete/', autocomplete, name='autocomplete'),
    path('list/exceldown/', exceldown, name='exceldown'),
    path('list/exceldel/', exceldel, name='exceldel'),
    path('list/upload/', upload, name='upload'),
    path('list/filedown/', filedown, name='filedown'),
]