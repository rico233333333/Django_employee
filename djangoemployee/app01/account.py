""" 登录模块 """
from django.shortcuts import redirect, render
from django import forms
from app01.models import Admin
import os,random

from app01.mode.encrypt import md5

class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",
                               widget=forms.TextInput(attrs={"class":"input-item","placeholder":"用户名"}),
                               required=True  # 必填不能为空
                               )
    password = forms.CharField(label="密码",
                               widget=forms.PasswordInput(attrs={"class":"input-item","placeholder":"密码"},render_value=True),
                               required=True
                               )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
def login(request):
    data_html = {}
    files = os.listdir("./app01/static/img/login_background_img")

    data_html["img"] = random.choice(files)
    data_html["img_f"] = random.choice(files)
    if request.method == "GET":
        form = LoginForm()
        data_html["form"] = form
        return render(request,"login2.html",data_html)
    # 如果是post请求
    form = LoginForm(data=request.POST)  # 数据验证
    if form.is_valid():
        data_html["form"] = form
        admin_object = Admin.objects.filter(username=form.cleaned_data["username"],password=form.cleaned_data['password']).first()
        print(bool(admin_object))
        if not admin_object:
            form.add_error("password","用户名或密码错误")  # 错误提示不够自己增加
            data_html["form"] = form
            return render(request, "login2.html", data_html)
        # 登录成功 COOKIE写入操作
        request.session["info"] = {"id":admin_object.id,"user_name":admin_object.username}
        return redirect("/admin_list/")  # 重定向
    data_html["form"] = form
    return render(request, "login2.html", data_html)

def loginout(request):
    """ 注销 """
    request.session.clear()
    return redirect("/login/")