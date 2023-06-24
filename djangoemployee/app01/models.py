from django.db import models


# Create your models here.

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='部门标题', max_length=32)  # verbose_name表示表的注解

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name='员工姓名', max_length=16)  # 创建了员工姓名
    password = models.CharField(verbose_name='密码', max_length=64)  # 创建员工密码
    age = models.IntegerField(verbose_name='年龄')  # 创建了年龄
    acount = models.DecimalField(verbose_name='余额', max_digits=10, decimal_places=2,
                                 default=0)  # 创建余额  decimal_places:设置小数位 max_digits = 10:设置这个最大位数
    create_time = models.DateField(verbose_name='入职时间')
    # django代码中带的约束
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    # 设置主键约束 只能是存在的ID  to表示与那张表关联 to_field 表示关联字段
    # 会在mysql字段后面加id  相当于depart_id
    # 部门被删除 
    '''
    1.级联删除 需要在字段后添加 on_delete = models.CASCADE
    depart = models.ForeignKey(to = 'Department',to_field = 'id',on_delete = models.CASCADE)
    2.删除置空
    depart = models.ForeignKey(to = 'Department',to_field = 'id',null = True,blank = True,on_delete = models.SET_NULL)
    '''
    depart = models.ForeignKey(verbose_name='部门', to='Department', to_field='id', null=True, blank=False,
                               on_delete=models.SET_NULL)


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号",max_length=32)
    price = models.IntegerField(verbose_name="价格")  # 价格不设置长度
    level_choice = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
        (5, "5级"),
        (6, "6级")
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choice,default=1)
    status_choice = (
        (1, "已占用"),
        (2, "未占用")
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choice,default=2)


class Admin(models.Model):
    """ 管理员账户表 """
    username = models.CharField(verbose_name="管理员账户名",max_length=32)
    password = models.CharField(verbose_name="管理员账户密码",max_length=64)