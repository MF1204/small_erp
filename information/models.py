from django.db import models


class Delivery(models.Model):
    delivery_id = models.AutoField(db_column='delivery_id', primary_key=True)
    delivery_name = models.CharField(db_column='delivery_name', max_length=50)
    delivery_price = models.IntegerField(db_column='delivery_price', default=0)

    class Meta:
        db_table = 'delivery'


class Pay_type(models.Model):
    pay_type_id = models.AutoField(db_column='pay_type_id', primary_key=True)
    pay_type_name = models.CharField(db_column='pay_type_name', max_length=50)

    class Meta:
        db_table = 'pay_type'


class Order_type(models.Model):
    order_type_id = models.AutoField(db_column='order_type_id', primary_key=True)
    order_type_sym = models.CharField(db_column='order_type_sym', max_length=1)
    order_type_name = models.CharField(db_column='order_type_name', max_length=50)

    class Meta:
        db_table = 'order_type'


class Boxing(models.Model):
    boxing_id = models.AutoField(db_column='boxing_id', primary_key=True)
    boxing_name = models.CharField(db_column='boxing_name', max_length=50)
    boxing_price = models.IntegerField(db_column='boxing_price', default=0)

    class Meta:
        db_table = 'boxing'


class Filling(models.Model):
    filling_id = models.AutoField(db_column='filling_id', primary_key=True)
    filling_name = models.CharField(db_column='filling_name', max_length=50)
    filling_price = models.IntegerField(db_column='filling_price', default=0)

    class Meta:
        db_table = 'filling'


class Sheet(models.Model):
    sheet_id = models.AutoField(db_column='sheet_id', primary_key=True)
    sheet_name = models.CharField(db_column='sheet_name', max_length=50)
    sheet_price = models.IntegerField(db_column='sheet_price', default=0)

    class Meta:
        db_table = 'sheet'


class Size(models.Model):
    size_id = models.AutoField(db_column='size_id', primary_key=True)
    product_id = models.ForeignKey('Product', related_name='size', on_delete=models.CASCADE, db_column='product_id')
    size_name = models.CharField(db_column='size_name', max_length=50)
    size_price = models.IntegerField(db_column='size_price', default=0)

    class Meta:
        db_table = 'size'


class Product(models.Model):
    product_id = models.AutoField(db_column='product_id', primary_key=True)
    category_id = models.ForeignKey('Category', related_name='product', on_delete=models.CASCADE,
                                    db_column='category_id')
    product_name = models.CharField(db_column='product_name', max_length=255)
    product_price = models.IntegerField(db_column='product_price', default=0)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.product_name


class Category(models.Model):
    category_id = models.AutoField(db_column='category_id', primary_key=True)
    category_big = models.CharField(db_column='category_big', max_length=50)
    category_mid = models.CharField(db_column='category_mid', max_length=50)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.category_mid, self.category_big