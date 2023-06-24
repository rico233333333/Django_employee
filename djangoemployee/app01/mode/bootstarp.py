""" BootStarp样式ModelForm处理类 """
from django import forms

class BootStarpModelForm(forms.ModelForm):
    """
    使用方法：
        class UserEditModelForm(BootStarpModelForm):  # 继承此类即可
            class Meta:  # 钩子方法(钟馗 百勾百中)
                model = UserInfo  # 此处UserInfo代指你在models方法里边儿创建的
                fields = ["name","password","age"]

    实在不会看这里：
        class AdminModelForm(BootStarpModelForm):
            class Meta:  # 钩子方法(钟馗 百勾百中)
                model = Admin  # 此处UserInfo代指你在models方法里边儿创建的
                fields = ["username", "password"]

        def admin_add(request):
            form = AdminModelForm()
            data_html = {}
            data_html["title"] = "新建管理员账户"
            data_html["form"] = form
            return render(request,"change.html",data_html)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for循环ModelForm中的所有字段，给每个字段插件设置
        for name, field in self.fields.items():
            # 字段中有属性，保留原来属性，没有属性才增加属性
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label,
                }
