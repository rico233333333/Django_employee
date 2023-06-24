""" 中间件类 """
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, render


class M1(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self,request):
        print("M1测试中间件 M1进来了")
        # 此方法没有返回值则代表可以一直往后走
        # 此处若是有返回值 则可以 类似视图函数那般返回一个特定页面或者返回某些数据
        # 可以返回render redirect

    def process_response(self,request,response):
        print("M1走了")
        return response

class M2(MiddlewareMixin):
    """ 中间件2 """

    def process_request(self,request):
        print("M2测试中间件 M2进来了")

    def process_response(self,request,response):
        print("M2走了")
        return response


class AuthMiddleware(MiddlewareMixin):

    def process_request(self,request):
        # 排除不需要登录就可以访问的页面
        # request.path_info  # 获取用户当前访问的url
        if request.path_info == "/login/":
            return # return None 可以让程序继续往后走
        # 读取用户session信息
        # 若是可以读取到，则代表用户登录过，就可以向后走
        # 若是没读取到，则返回login登陆页面
        info_dict = request.session.get("info")
        if info_dict:
            return

        return redirect("/login/")
