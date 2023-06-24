from django.contrib import admin
from django.shortcuts import redirect, render
from app01.models import Admin
from django.core.exceptions import ValidationError  # 报错信息提示模块
from django import forms

from app01.mode.pagination import Pagination
from app01.mode.encrypt import md5
from app01.mode.bootstarp import BootStarpModelForm

# Register your models here.

def admin_list(request):
    """ 管理员列表 """
    # cookie处理 中间件
    # 用户发来请求 获取cookie随机字符串，拿着随机字符串看看session中有没有
    # 若是cookie被动的在浏览器删除则返回None
    # request.session.get("info")
    info = request.session.get("info")
    # print(info)  # 此处返回字典 {'id': 12, 'user_name': 'ricardo'}  若是浏览器Cookie被被动删除则自处返回状态为空(None)



    value = request.GET.get('username', None)
    dict_data = {}
    dict_data["username__contains"] = str(value)

    page = int(request.GET.get('page', 1))  # 此处获取用户输入的页码没有页码返回1
    page_num = int(request.GET.get('page_num', 10))  # 此处获取用户输入的
    if value == None:
        queryset = Admin.objects.all()
    else :
        queryset = Admin.objects.filter(**dict_data)
    pagination = Pagination(request=request, page=page, page_num=page_num, value=value, queryset=queryset)
    page_html = pagination.page_html()

    return render(request, "admin_list.html",
                  {"queryset":queryset,"pre": page_html[0], "page_string": page_html[1], "page_num_string": page_html[2]})

class AdminModelForm(BootStarpModelForm):
    confirm_password = forms.CharField(label="确认密码",
                                       widget = forms.PasswordInput,
                                       # widget = forms.PasswordInput(render_value=True)  此处表示不想清空用户输入的数据
                                       )  # 方法1 密码框
    class Meta:  # 钩子方法(钟馗 百勾百中)
        model = Admin  # 此处UserInfo代指你在models方法里边儿创建的
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password":forms.PasswordInput  # 方法二 密码框
            # 若是提交错误后不想清空输入框 则 "password":forms.PasswordInput(render_value=True)
        }

    def clean_confirm_password(self):
        # 钩子方法
        user = self.cleaned_data.get("username")
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        username_bool = Admin.objects.filter(username=user).exists()
        if md5(confirm) != pwd:
            raise ValidationError("密码不一致请重新输入")
        if username_bool == True:
            raise ValidationError("已存在该管理员 请重新创建")
        return confirm  # 此处钩子方法返回的值会 传入到form里边 仅是获取用户输入

    def clean_password(self):
        # 钩子方法
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_username(self):
        # 钩子方法
        user = self.cleaned_data.get("username")
        username_bool = Admin.objects.filter(username=user).exists()

        if username_bool == True:
            raise ValidationError("已存在该管理员 请重新创建")
        return user  # 此处钩子方法返回的值会 传入到form里边 仅是获取用户输入


def admin_add(request):
    """ 新建管理员 """
    data_html = {}
    data_html["title"] = "新建管理员账户"

    if request.method == "GET":
        form = AdminModelForm()
        data_html["form"] = form
        return render(request,"change.html",data_html)

    form = AdminModelForm(data = request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin_list/")
    data_html["form"] = form
    return render(request,"change.html",data_html)

class AdminEditModelForm(BootStarpModelForm):
    class Meta:  # 钩子方法(钟馗 百勾百中)
        model = Admin  # 此处UserInfo代指你在models方法里边儿创建的
        fields = ["username"]


def admin_edit(request,nid):
    """ 编辑管理员 """
    data_html = {}
    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        data_html["msg"] = "您所访问的数据不存在或已删除请您务必及时刷新页面"
        return render(request,"error.html",data_html)
    data_html["title"] = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        data_html["form"] = form
        return render(request, "change.html", data_html)
    form = AdminEditModelForm(data=request.POST,instance=row_object)
    if form.is_valid():  # 此处进行数据校验
        form.save()
        return redirect("/admin_list/")
    return render(request,"error.html",data_html)


def admin_del(request,nid):
    """ 删除管理员 """
    a = Admin.objects.filter(id=nid).delete()
    print(a)
    return redirect("/admin_list/")

class AdminResetModelForm(BootStarpModelForm):
    confirm_password = forms.CharField(label="确认密码",
                                       # widget=forms.PasswordInput,
                                       widget = forms.PasswordInput(render_value=True)  # 此处表示不想清空用户输入的数据
                                       )  # 方法1 密码框

    class Meta:  # 钩子方法(钟馗 百勾百中)
        model = Admin  # 此处UserInfo代指你在models方法里边儿创建的
        fields = ["password","confirm_password"]
        widgets = {
            # "password": forms.PasswordInput  # 方法二 密码框
            "password":forms.PasswordInput(render_value=True)  # 若是提交错误后不想清空输入框 则
        }

    def clean_confirm_password(self):
        # 钩子方法
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if md5(confirm) != pwd:
            raise ValidationError("密码不一致请重新输入")
        return confirm  # 此处钩子方法返回的值会 传入到form里边 仅是获取用户输入

    def clean_password(self):
        # 钩子方法
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        # 数据库校验
        exists = Admin.objects.filter(id = self.instance.pk, password = md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前输入的一致")
        return md5_pwd

def admin_reset(request,nid):
    """ 重置密码 """
    data_html = {}
    row_object = Admin.objects.filter(id=nid).first()

    if not row_object:
        data_html["msg"] = "您所访问的数据不存在或已删除请您务必及时刷新页面"
        return render(request, "error.html", data_html)

    if request.method == "GET":
        form = AdminResetModelForm()
        data_html["title"] = f"重置密码 -》{row_object.username}"
        data_html["form"] = form
        return render(request, "change.html", data_html)

    form = AdminResetModelForm(data=request.POST,instance=row_object)

    if form.is_valid():
        form.save()
        return redirect("/admin_list/")

    data_html["title"] = f"重置密码 -》{row_object.username}"
    data_html["form"] = form
    return render(request, "change.html", data_html)