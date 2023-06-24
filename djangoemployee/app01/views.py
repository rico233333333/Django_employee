from app01.models import Department, UserInfo, PrettyNum
from django.shortcuts import redirect, render
from app01.mode.pagination import Pagination

# Create your views here.

# 部门管理


def depart_list(request):
    """
    部门管理页
    """
    # 获取所有的部门
    depart_list = Department.objects.all()
    return render(request, 'dedpart_list.html', {'depart_list': depart_list})


def depart_add(request):
    """
    增加部门
    """
    # 增加部门
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    elif request.method == 'POST':
        Department.objects.create(title=request.POST['new_department'])
        return redirect('/depart_list/')


def depart_del(request):
    '''
    删除部门
    '''
    # 获取ID
    nid = request.GET.get('nid')
    # return render('')
    # 删除
    Department.objects.filter(id=nid).delete()


    # 重定向
    return redirect('/depart_list')


def depart_edit(request, nid):
    '''
    修改部门
    '''
    # 修改部门
    if request.method == 'GET':
        department_edit_row = Department.objects.filter(
            id=nid).first()  # 取匹配到的第一个数据
        return render(request, 'depart_edit.html', {'title': department_edit_row.title})
    elif request.method == 'POST':
        Department.objects.filter(id=nid).update(
            title=request.POST['new_department'])
        return redirect('/depart_list/')


def index(request):
    return render(request, 'index.html')


def user_list(request):
    ''' 用户管理 '''
    user_list_ = UserInfo.objects.all()
    # user_list_ = []
    # for user_data in UserInfo.objects.all():
    #     user_data_list = [user_data.id,user_data.name,user_data.age,user_data.acount,user_data.create_time.strftime("%Y-%M-%D"),user_data.get_gender_display(),user_data.depart.title]
    #     user_list_.append(user_data_list)
    #     # print(user_data.get_gender_display())  # get_字段名_display拿取封装数据
    #     '''
    #     跨表查询第一种方法
    #     Department.objects.filter(id=user_data.depart).first().title

    #     第二种方法(多表练级查询)
    #     user_data.depart
    #     获取属性值
    #     user_data.depart.title
    #     '''
    return render(request, 'user_list.html', {'user_list_': user_list_})  # type: ignore


def user_add(request):
    '''增加用户'''
    if request.method == "GET":
        context = {
            'gender_choices': UserInfo.gender_choices,
            'depart_list': Department.objects.all()
        }

        return render(request, 'user_add.html', context)
    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        age = request.POST.get('age')
        acount = request.POST.get('ac')
        ctime = request.POST.get('time')
        gender = request.POST.get('gd')
        depart_id = request.POST.get('dp')
        UserInfo.objects.create(name=user, password=pwd, age=age, acount=acount, create_time=ctime, gender=gender,
                                depart_id=depart_id)

        return redirect('/user_list')


# 创建modelform类
from django import forms


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label="用户名")  # 此处方法重写定义字段长度

    class Meta:
        model = UserInfo
        fields = ['name', 'password', 'age', 'acount', 'create_time', 'gender', 'depart']
        # widgets = {  # 若是想改变样式也可以选择这个
        #     "name":forms.TextInput(attrs={'class':'col-sm-12'}),
        #     "password":forms.PasswordInput(attrs={'class':'col-sm-12'})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class=""
        for name, field in self.fields.items():
            if name == "password":  # 下方widget表示插件
                field.widget.attrs = {"type":"password", "class": "col-sm-12 form-control", "id": "exampleInputPassword3"}
            elif name == "gender" or "depart":
                field.widget.attrs = {"class": "col-sm-12 form-control"}
            field.widget.attrs = {"class": "col-sm-12 form-control", "placeholder": "请输入"+str(field.label)}


def user_add_modelform(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_add_modelform.html", {"form": form})
    else:
        # 用户使用POST 发送的数据必须经过数据校验
        form = UserModelForm(data=request.POST)
        if form.is_valid():  # form.is_valid() 此处进行数据校验
            # 提交成功
            # print(form.cleaned_data)  # 打印所有的数据
            form.save()
            return redirect('/user_list/')
        else:
            # print(form.errors)  # 若是错误就打印错误信息
            return render(request, "user_add_modelform.html", {"form": form})

def user_del(request):
    nid = request.GET.get('nid')
    # return render('')
    # 删除
    UserInfo.objects.filter(id=nid).delete()

    # 重定向
    return redirect('/user_list')

def user_edit(request,nid):
    row_object = UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_object)  # 显示默认数据
        return render(request,'user_edit.html',{'form':form})
    else :
        # 用户使用POST 发送的数据必须经过数据校验
        form = UserModelForm(data=request.POST,instance=row_object)
        if form.is_valid():  # form.is_valid() 此处进行数据校验
            # 提交成功
            # print(form.cleaned_data)  # 打印所有的数据
            # 若是想要在用户输入以外额外的增加一些值 则可以
            # form.instance.字段名字 = "值" 即可
            form.save()  # 默认保存用户提交的所有数据
            return redirect('/user_list/')
        else:
            # print(form.errors)  # 若是错误就打印错误信息
            return render(request, "user_edit.html", {"form": form})

def pretynum_list(request):
    # 分页查询组件封装
    from django.http.request import QueryDict  # 此处是对此对象的字段进行更改
    # import copy
    # get_quere_dict = copy.deepcopy(request.GET)  # 此处进行深拷贝
    # get_quere_dict._mutable = True  # 此处更改此字段值为True

    # get_quere_dict.setlist('q',[11])
    # print(get_quere_dict.urlencode())

    dict_data = {}
    value = request.GET.get('q',1)
    dict_data["mobile__contains"] = str(value)

    page = int(request.GET.get('page',1))  # 此处获取用户输入的页码没有页码返回1
    page_num = int(request.GET.get('page_num',10))  # 此处获取用户输入的
    if value == None:
        queryset = PrettyNum.objects.all().order_by("-level")
    else :
        queryset = PrettyNum.objects.filter(**dict_data).order_by("-level")
    pagination = Pagination(request=request,page=page,page_num=page_num,value = value,queryset = queryset)
    page_html = pagination.page_html()

    return render(request,"pretynum_list.html", {"pre":page_html[0],"page_string":page_html[1],"page_num_string":page_html[2]})

from django.core.validators import RegexValidator  # 方式1正则判断
from django.core.validators import ValidationError  # 方式2

# 定义靓号操作管理类
class PretyModelForm(forms.ModelForm):
    """ 靓号操作类 """
    # mobile = forms.CharField(
    #     label="手机靓号",
    #     validators=[RegexValidator(r"^q[3-9]\d{9}$","手机格式错误")]
    # )

    class Meta:
        model = PrettyNum
        fields = ["mobile","price","level","status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class=""
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "col-sm-12 form-control", "placeholder": "请输入"+str(field.label)}

    def clean_mobile(self):  # 此处函数命名为 clean_字段名
        txt_mobile = self.cleaned_data["mobile"]  # 此处获取输入
        if len(txt_mobile) != 11:  # 用户输入出错
            raise ValidationError("格式错误")
        exists = PrettyNum.objects.filter(mobile=txt_mobile).exists()  # 此处判断提交字段是否存在 返回bools
        if exists ==  True:
            raise ValidationError("号码已存在 请重新输入号码")
        return txt_mobile  # 若是没问题则返回用户输入的值



def pretynum_add(request):
    """ 添加靓号 """
    if request.method == "GET":
        form = PretyModelForm()
        return render(request, "pretty_add.html",{'form':form})
    else :
        form = PretyModelForm(data=request.POST)
        if form.is_valid():  # form.is_valid() 此处进行数据校验
            # 提交成功
            # print(form.cleaned_data)  # 打印所有的数据
            form.save()
            return redirect('/pretynum_list/')
        else:
            # print(form.errors)  # 若是错误就打印错误信息
            return render(request, "pretty_add.html", {"form": form})


# 靓号编辑modelform
# 定义靓号操作管理类
class PretyEditModelForm(forms.ModelForm):
    """ 靓号操作类 """
    # 设置某字段不可编辑
    mobile = forms.CharField(disabled=True,label="手机号")

    # mobile = forms.CharField(
    #     label="手机靓号",
    #     validators=[RegexValidator(r"^q[3-9]\d{9}$","手机格式错误")]
    # )

    class Meta:
        model = PrettyNum
        fields = ["mobile","price","level","status"] # 此处设置好展示字段
        # 设置手机号字段不展示
        # fields = ["price","level","status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class=""
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "col-sm-12 form-control", "placeholder": "请输入"+str(field.label)}

    def clean_mobile(self):  # 此处函数命名为 clean_字段名
        txt_mobile = self.cleaned_data["mobile"]  # 此处获取输入
        if len(txt_mobile) != 11:  # 用户输入出错
            raise ValidationError("格式错误")
        # self.instance.pk 获取当前编辑值
        exists = PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile)  # 此处判断排除自己以外与其他手机号是否重复
        if exists == True:
            raise ValidationError("号码已存在 请重新输入号码")
        return txt_mobile  # 若是没问题则返回用户输入的值

def pretynum_edit(request,nid):
    row_object = PrettyNum.objects.filter(id = nid).first()
    if request.method == "GET":
        form = PretyEditModelForm(instance=row_object)  # 显示默认数据
        return render(request, "pretty_edit.html",{"form":form})
    else :
        form = PretyEditModelForm(data=request.POST, instance=row_object)
        if form.is_valid():  # form.is_valid() 此处进行数据校验
            # 提交成功
            # print(form.cleaned_data)  # 打印所有的数据
            # 若是想要在用户输入以外额外的增加一些值 则可以
            # form.instance.字段名字 = "值" 即可
            form.save()  # 默认保存用户提交的所有数据
            return redirect('/pretynum_list/')
        else:
            # print(form.errors)  # 若是错误就打印错误信息
            return render(request, "pretty_edit.html", {"form": form})

def pretynum_del(request):
    nid = request.GET.get('nid')
    # return render('')
    # 删除
    PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretynum_list/")

