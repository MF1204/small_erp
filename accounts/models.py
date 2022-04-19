from django.db import models


class Member(models.Model):
    member_no = models.AutoField(db_column='member_no', primary_key=True)
    member_id = models.CharField(db_column='member_id', max_length=20)
    member_pw = models.CharField(db_column='member_pw', max_length=50)
    member_name = models.CharField(db_column='member_name', max_length=50)
    member_rank = models.CharField(db_column='member_rank', max_length=50, default='사원')
    member_auth = models.CharField(db_column='member_auth', max_length=20, default='조회')
    hiredate = models.DateField(db_column='hiredate')
    resignationdate = models.DateField(db_column='resignationdate', null=True)
    register_date = models.DateTimeField(db_column='register_date', )
    access_latest = models.DateTimeField(db_column='access_latest', )

    class Meta:
        db_table = 'member'
