from django.contrib import admin
from app01.models import Department,UserInfo,PrettyNum,Admin
 
# Register your models here.
admin.site.register([Department,UserInfo,PrettyNum,Admin])