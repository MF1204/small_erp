from django.db import models
from datetime import datetime
# Create your models here.


class Order(models.Model):
    pno = models.AutoField(db_column='pno', primary_key=True)
    order_no = models.CharField(db_column='order_no', max_length=20)
    date_no = models.IntegerField(db_column='date_no')
    employee_name = models.CharField(db_column='employee_name', max_length=50)
    order_date = models.DateField(db_column='order_date', auto_now=False)
    customer = models.CharField(db_column='customer', max_length=50)
    customer_phone = models.CharField(db_column='customer_phone', max_length=11)
    order_type_name = models.CharField(db_column='order_type', max_length=50)
    pay_type_name = models.CharField( db_column='pay_type', max_length=50)
    pay_check = models.CharField(db_column='pay_check', max_length=1)
    product_name = models.CharField(db_column='product_name', max_length=50)
    state = models.CharField(db_column='state', max_length=20)
    receipt_date = models.DateField(db_column='receipt_date',)
    receipt_hour = models.TimeField(db_column='receipt_hour',)
    size_option_name = models.CharField(db_column='size_name', max_length=50)
    sheet_option_name = models.CharField(db_column='sheet_name', max_length=50)
    filling_option_name = models.CharField(db_column='filling_name', max_length=50)
    boxing_option_name = models.CharField(db_column='boxing_name', max_length=50)
    count = models.IntegerField(db_column='count')
    total_price = models.IntegerField(db_column='total_price', )
    product_price = models.IntegerField(db_column='product_price', )
    recipient = models.CharField(db_column='recipient', max_length=50)
    recipient_phone = models.CharField(db_column='recipient_phone', max_length=11)
    delivery_option_name = models.CharField(db_column='delivery_name', max_length=50)
    address1 = models.TextField(db_column='address1', )
    address2 = models.TextField(db_column='address2', )
    phrase = models.TextField(db_column='phrase', )
    memo = models.TextField(db_column='memo', )
    cafe24_no = models.CharField(db_column='cafe24_no', max_length=16)
    usage_flag = models.IntegerField(db_column='usage_flag', null=False, default='1')

    class Meta:
        db_table = 'order'

    def __str__(self):
        return self.pay_check
