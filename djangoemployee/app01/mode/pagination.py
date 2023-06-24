"""
此文件封装分页组件
"""
from django.utils.safestring import mark_safe
class Pagination:
    """
    分页组件封装

    需要传参：
        requests:Django视图文件函数传参必传
        page:页码
        queryset:数通过搜索框查询到的据集合 用于统计数量
        value:通过搜索框查询到的数据 反馈到页面

    对应python函数中
        def pretynum_list(request):
            # 分页查询组件封装
            from django.http.request import QueryDict  # 此处是对此对象的字段进行更改
            # import copy
            # get_quere_dict = copy.deepcopy(request.GET)  # 此处进行深拷贝
            # get_quere_dict._mutable = True  # 此处更改此字段值为True

            # get_quere_dict.setlist('q',[11])
            # print(get_quere_dict.urlencode())

            dict_data = {}
            value = request.GET.get('q',None)
            print(value)
            dict_data["mobile__contains"] = str(value)

            page = int(request.GET.get('page',1))  # 此处获取用户输入的页码没有页码返回1
            page_num = int(request.GET.get('page_num',10))  # 此处获取用户输入的
            queryset = PrettyNum.objects.filter(**dict_data).order_by("-level")
            pagination = Pagination(request=request,page=page,page_num=page_num,value = value,queryset = queryset)
            page_html = pagination.page_html()

            return render(request,"pretynum_list.html", {"pre":page_html[0],"page_string":page_html[1],"page_num_string":page_html[2]})

    对应html文件中  此处只需要接受字符串即可
        <ul class="pagination">
            {{ page_string }}
        </ul>
    """
    def __init__(self,request,page,queryset,value,page_num=10):
        from django.http.request import QueryDict  # 此处是对此对象的字段进行更改
        # import copy
        # get_query_dict = copy.deepcopy(request.GET)  # 此处进行深拷贝
        # get_query_dict._mutable = True  # 此处更改此字段值为True
        # self.query_dict = get_query_dict
        # self.get_query_dictget_query_dict.setlist('q', [11])
        # print(get_query_dict.urlencode())  # 此处获取URL所有参数
        # self.get_query_dict
        self.page = page  # 实例化属性
        self.page_num = page_num
        self.value = value
        self.queryset = queryset  # 此处接收quereset对象
        self.start_page = (self.page-1) * self.page_num
        self.end_page = self.page * self.page_num
        self.pre_count = self.queryset.count()  # 此处记录总数
        self.prety = self.queryset[self.start_page:self.end_page]
        self.pre_count , yv = divmod(self.pre_count,self.page_num)
        if yv:
            self.pre_count += 1
        self.plus = 5
        if self.pre_count <= 2 * self.plus + 1:
            self.start_page = 1
            self.end_page = self.pre_count
        else:
            if self.page <= self.plus:
                self.start_page = 1
                self.end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.pre_count:
                    self.start_page = self.pre_count - 2 * self.plus
                    self.end_page = self.pre_count + 1
                else:
                    self.start_page = self.page - self.plus
                    self.end_page = self.page + self.plus + 1

    def page_html(self):
        self.page_list = []
        self.page_list.append(f'<li class=""><a href="?q={self.value}&page={1}&page_num={self.page_num}">首页</a></li>')
        if self.page > 1:
            self.page_list.append(f'<li class=""><a href="?q={self.value}&page={self.page - 1}&page_num={self.page_num}">上一页</a></li>')
        else:
            self.page_list.append(f'<li class=""><a href="?q={self.value}&page=1&page_num={self.page_num}">上一页</a></li>')
        for i in range(self.start_page, self.end_page):
            if i == self.page:
                self.page_list.append(f'<li class="active"><a href="?q={self.value}&page={i}&page_num={self.page_num}">{i}</a></li>')
            else:
                self.page_list.append(f'<li><a href="?q={self.value}&page={i}&page_num={self.page_num}">{i}</a></li>')
        if self.page < self.pre_count:
            self.page_list.append(f'<li class=""><a href="?q={self.value}&page={self.page + 1}&page_num={self.page_num}">下一页</a></li>')
        else:
            self.page_list.append(f'<li class=""><a href="?q={self.value}&page={self.page}&page_num={self.page_num}">下一页</a></li>')
        self.page_list.append(f'<li class=""><a href="?q={self.value}&page={self.pre_count}&page_num={self.page_num}">尾页</a></li>')
        self.page_string = mark_safe("".join(self.page_list))  # 将生成的字符串保证他的安全

        self.page_num_list = []
        for i in range(5, 21, 5):
            if self.page_num == i:
                self.page_num_list.append(f'<option value="{i}" selected>{i}条</option>')
            else:
                self.page_num_list.append(f'<option value="{i}">{i}条</option>')
        self.page_num_string = mark_safe("".join(self.page_num_list))  # 将生成的字符串保证他的安全
        return [self.prety,self.page_string,self.page_num_string]