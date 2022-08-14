from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, ListModelMixin, \
    CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from app01.app_permission import UserPermission
from app01.models import Book, User, Permissions, Role
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from app01.bookserializer import BookSerializer, BookModelSerializer, UserSerializer, RoleSerializer, \
    PermissionSerializer
from rest_framework.response import Response

# 定义BookView视图，用来处理Bookview的函数
class BookView(APIView):
    def post(self, request):
        """
        增加数据
        1.直接将request.data放到serializer中，返回反序列化对象
        2.调用序列化对象的is_valid方法（is_valid规则在序列化类中重写），验证数据是否合法
        3。若合法，调用序列化对象的save方法（需要在serializer类中重写create方法），若不合法，则需要返回序列化对象的.errors方法，告诉哪儿出错了
        :param request:
        :return:
        """
        response_msg = {'status': 100, 'msg': '成功'}
        # 修改才有instance，新增没有instance，只有data
        book_ser = BookSerializer(data=request.data)
        # book_ser = BookSerializer(request.data)  # 这个按位置传request.data会给instance，就报错了
        # 校验字段
        if book_ser.is_valid():
            book_ser.save()  # 回调用create方法
            response_msg['data'] = book_ser.data
        else:
            response_msg['status'] = 102
            response_msg['msg'] = '数据校验失败'
            response_msg['data'] = book_ser.errors
        return Response(response_msg)

    def get(self, request, pk):
        """
        获取单个数据
        1. 首先在数据库中用orm找到数据对象
        2. 将数据对象传到序列化类中，进行序列化
        3. 序列化对象的.data就是序列化后的json数据
        :param request:
        :param pk:
        :return:
        """
        book = Book.objects.filter(id=pk).first()
        # 用一个类，毫无疑问，一定要实例化
        # 要序列化谁，就把谁传过来
        book_ser = BookModelSerializer(book)  # 调用类的__init__
        # book_ser.data   序列化对象.data就是序列化后的字典
        return Response(book_ser.data)
        # return JsonResponse(book_ser.data)

    def put(self, request, pk):
        """
        修改数据
        1.首先在数据库中找到需要修改的数据对象
        2.将需要修改的数据对象和修改的数据都传递给serializer类，并返回修改后的序列化对象
        3.通过序列化对象的is_valid()方法验证修改后的序列化对象是否合法（需要在serializer类中重写update方法，告诉框架什么数据和什么数据对应）
        4.若合法则调用序列化对象的save方法，若不合法则调用序列化对象的errors方法查看详情
        :param request:
        :param pk:
        :return:
        """
        response_msg = {'status': 100, 'msg': '成功'}
        # 找到这个对象
        book = Book.objects.filter(id=pk).first()
        # 得到一个序列化类的对象
        # boo_ser=BookSerializer(book,request.data)
        boo_ser = BookSerializer(instance=book, data=request.data)

        # 要数据验证（回想form表单的验证）
        if boo_ser.is_valid():  # 返回True表示验证通过
            boo_ser.save()  # 报错 需要调用update方法
            response_msg['data'] = boo_ser.data
        else:
            response_msg['status'] = 101
            response_msg['msg'] = '数据校验失败'
            response_msg['data'] = boo_ser.errors

        return Response(response_msg)

    def delete(self, request, pk):
        """
        删除指定数据
        :param request:
        :param pk:
        :return:
        """
        ret = Book.objects.filter(pk=pk).delete()
        return Response({'status': 100, 'msg': '删除成功'})


class BooksView(APIView):
    """
    获取多个数据
    1. 用orm获取想要的数据
    2. 将数据对象集传到serializer类中，加上many属性
    """

    def get(self, request):
        response_msg = {'status': 100, 'msg': '成功'}
        books = Book.objects.all()
        book_ser = BookSerializer(books, many=True)
        print(book_ser)# 序列化多条,如果序列化一条，不需要写
        response_msg['data'] = book_ser.data
        return Response(response_msg)


"""
以上，简要得介绍了APIView的基础用法，以及大概使用步骤和需要注意的地方，
接下来介绍一个更方便的用法 =》 GenericAPIView类

1. 为什么会有GenericAPIView类？
从上面可以看出，我们会一直重复得写Book.objects.all()和BookSerializer()这些方法，这是很不规范的，应该在每一个View类中需要序列化的模型和序列化类
都是提前指定好的，另外可以发现几乎所有的view都是按上面写的，重复性太高，使用GenericAPIView类主要是为了和mixin类进行配合使用，drf作者将重复的东西
都给我们封装好了大大方便代码书写

2.GenericAPIView与APIView区别？
其实两者区别不大，只不过GenericAPIView可以配合mixin使用，从而减少代码量

具体使用方法如下
"""


class Book2View(GenericAPIView):
    # queryset要传queryset对象，查询了所有的图书
    # serializer_class使用哪个序列化类来序列化这堆数据
    queryset = Book.objects.all()
    # queryset=Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        book_list = self.get_queryset()  # 获取多个使用get_queryset()方法
        book_ser = self.get_serializer(book_list, many=True)

        return Response(book_ser.data)

    def post(self, request):
        book_ser = self.get_serializer(data=request.data)
        if book_ser.is_valid():
            book_ser.save()
            return Response(book_ser.data)
        else:
            return Response({'status': 101, 'msg': '校验失败', 'errors': book_ser.errors})


class Book2DetailView(GenericAPIView):
    queryset = Book.objects
    serializer_class = BookSerializer

    def get(self, request, pk):
        book = self.get_object()
        book_ser = self.get_serializer(book)
        return Response(book_ser.data)

    def put(self, request, pk):
        book = self.get_object()  # 获取单个用get_object()方法
        book_ser = self.get_serializer(instance=book, data=request.data)
        if book_ser.is_valid():
            book_ser.save()
            return Response(book_ser.data)
        else:

            return Response({'status': 101, 'msg': '校验失败', 'errors': book_ser.errors})

    def delete(self, request, pk):
        ret = self.get_object().delete()
        return Response({'status': 100, 'msg': '删除成功'})


"""
GenericAPIView与5个mixin类共同使用
"""


class Book3View(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Book.objects
    serializer_class = BookSerializer

    def get(self, request):
        """
        查询所有
        :param request:
        :return:
        """
        return self.list(request)

    def post(self, request):
        """
        增加一条数据
        :param request:
        :return:
        """
        return self.create(request)  # create会自动帮我们验证和保存数据


class Book3DetailView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin):
    queryset = Book.objects
    serializer_class = BookSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)  # 查询单个

    def put(self, request, pk):
        return self.update(request, pk)  # 更新单个

    def delete(self, request, pk):
        return self.destroy(request, pk)


"""
可以发现，上面直接返回了作者封装的代码，确确实实减少了代码量，
但是容易发现，代码依然有重复多余，每次都要自己return出去，明显很麻烦，所以作者为了方便，又给我们封装了一层，将GenericAPIView类与其他mixin类
一起封装为一个类
        CreateAPIView,
        ListAPIView,
        UpdateAPIView,
        RetrieveAPIView,
        DestroyAPIView,
        ListCreateAPIView,
        RetrieveUpdateDestroyAPIView,
        RetrieveDestroyAPIView,
        RetrieveUpdateAPIView
分别为
CreateAPIView
提供 post 方法
继承自： GenericAPIView、CreateModelMixin

ListAPIView
提供 get 方法
继承自：GenericAPIView、ListModelMixin

RetrieveAPIView
提供 get 方法
继承自: GenericAPIView、RetrieveModelMixin

DestoryAPIView
提供 delete 方法
继承自：GenericAPIView、DestoryModelMixin

UpdateAPIView
提供 put 和 patch 方法
继承自：GenericAPIView、UpdateModelMixin

ListCreateAPIView
提供 get 和 post方法
继承自 GenericAPIView，ListModelMixin,CreateModelMixin

RetrieveUpdateAPIView
提供 get、put、patch方法
继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin

RetrieveUpdateDestoryAPIView
提供 get、put、patch、delete方法
继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestoryModelMixin

"""


class Books4View(ListCreateAPIView):  # 注意单个只能用Retrieve,Create相关的APIView
    serializer_class = BookSerializer
    queryset = Book.objects


class Book4View(RetrieveUpdateAPIView):  # 非单个不能使用Retrieve,Create相关的APIView，不然会方法冲突
    serializer_class = BookSerializer
    queryset = Book.objects


"""
很明显上面代码量更少，分装的更彻底
但是，也依然不够完美，明明是同一套视图，却要使用两个类来处理，这很明显是不合常理的
drf 作者也想到了 于是，就有了视图集 （ViewSet）的概念，将两套视图类合到一个类中

使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：

list() 提供一组数据
retrieve() 提供单个数据
create() 创建数据
update() 保存数据
destory() 删除数
"""


class Book5ViewSet(viewsets.ViewSet):

    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            books = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(books)
        return Response(serializer.data)


"""
使用ViewSet通常并不方便，因为list、retrieve、create、update、destory等方法都需要自己编写，而这些方法与前面讲过的Mixin扩展类提供的方法同名，所以我们可以通过继承Mixin扩展类来复用这些方法而无需自己编写。但是Mixin扩展类依赖与GenericAPIView，所以还需要继承GenericAPIView。

GenericViewSet就帮助我们完成了这样的继承工作，继承自GenericAPIView与ViewSetMixin，在实现了调用as_view()时传入字典（如{'get':'list'}）的映射处理工作的同时，还提供了GenericAPIView提供的基础方法，可以直接搭配Mixin扩展类使用。
"""

# TODO 这是最简化版的 视图集  推荐使用

class Book6ViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


"""
当需要以上五个接口时，可以直接使用ModelViewSet类，不过此时url写法上有些改变
"""


# 自定义分页行为
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3  # 默认每页显示多少条
    page_size_query_param = 'page_size'  # 控制每页显示多少条
    max_page_size = 1000  # 前端设置最大为1000
    # http://127.0.0.1:8000/books7/?page_size=2前端通过page_size来确定访问每页多大


from rest_framework.filters import OrderingFilter
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, JWTAuthentication


class Book6ModelView(ModelViewSet):  # 5个接口都有，但是路由有点问题
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    """
    认证方案
    
    只是认证为 什么身份 而不能限制用户操作
    """
    authentication_classes = [JWTAuthentication]
    # 设置允许的请求方法
    # http_method_names = ("post", "patch")
    """
    权限方案  
    IsAuthenticated 只要登录了才能访问
    """
    permission_classes = [IsAuthenticated, UserPermission]

    # 限流
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    """
    设置过滤字段，需要提前安装django-filters
    然后注册django-filters，
    在设置中全局配置  
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
    """
    filter_fields = ('name',)

    """设置排序字段，需要提前引入from rest_framework.filters import OrderingFilter
        访问时使用  
        127.0.0.1:8000/books/?ordering=-bread
    """
    filter_backends = [OrderingFilter, DjangoFilterBackend]  # 过滤后再排序
    ordering_fields = ('id', 'price')  # 排序字段
    # pagination_class = LargeResultsSetPagination  # 分页方案


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 局部取消身份验证和权限验证
    authentication_classes = []
    permission_classes = []

    def perform_update(self, serializer):
        # 获取用户对象
        user = self.get_object()
        try:
            roles = self.request.data["role"]
            if len(roles) > 0:
                user.role.clear()
                for role in roles:
                    print(role)
                    role = Role.objects.filter(role_name=role).first()
                    user.role.add(role)
                    print("ok")
        except Exception:
            pass
        serializer.save()


# 权限类
class PermissionView(ModelViewSet):
    queryset = Permissions.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# 角色类
class RoleView(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = []
    permission_classes = []

    # def perform_create(self, serializer):
    #     pass
    filter_fields = ['role_name']
    def perform_update(self, serializer):
        role = self.get_object()
        try:
            permissions = self.request.data["permissions"]
            if len(permissions) > 0:
                role.permission.clear()
                for permission in permissions:
                    print(permission)
                    permission = Permissions.objects.filter(permission_name=permission).first()
                    role.permission.add(permission)
        except Exception:
            pass
        serializer.save()
