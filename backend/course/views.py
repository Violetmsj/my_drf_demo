from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CourseSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # Django的信号机制
def generate_token(sender, instance=None, created=False, **kwargs):
    """
    创建用户时自动生成Token
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        Token.objects.create(user=instance)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # 仅使当前请求携带的 Token 失效，不影响其他认证方式。
        if request.auth:
            request.auth.delete()
        return Response({"detail": "退出登录成功"}, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


"""一、 函数式编程 Function Based View"""


@api_view(["GET", "POST"])
@authentication_classes(
    (BasicAuthentication, SessionAuthentication, TokenAuthentication)
)
@permission_classes((IsAuthenticated,))
def course_list(request):
    """
    获取所有课程信息或新增一个课程
    :param request:
    :return:
    """
    if request.method == "GET":
        s = CourseSerializer(instance=Course.objects.all(), many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        s = CourseSerializer(data=request.data)  # 部分更新用partial=True属性
        if s.is_valid():
            s.save(teacher=request.user)
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes(
    (BasicAuthentication, SessionAuthentication, TokenAuthentication)
)
@permission_classes((IsAuthenticated,))
def course_detail(request, pk):
    """
    获取、更新、删除一个课程
    :param request:
    :param pk:
    :return:
    """
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(
            data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND
        )
    else:
        if request.method == "GET":
            s = CourseSerializer(instance=course)
            return Response(data=s.data, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            s = CourseSerializer(instance=course, data=request.data)
            if s.is_valid():
                s.save()
                return Response(data=s.data, status=status.HTTP_200_OK)
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


"""二、 类视图 Class Based View"""


class CourseList(APIView):
    permission_classes = (IsAuthenticated,)  # settings.py中已设置，此处是多余的

    def get(self, request):
        """
        :param request:
        :return:
        """
        queryset = Course.objects.all()
        s = CourseSerializer(instance=queryset, many=True)  # 这里是instance = xx
        # s = CourseSerializer(instance=queryset.first())
        return Response(s.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        :param request:
        :return:
        """
        s = CourseSerializer(
            data=request.data
        )  # 这里是data = xx, return前要先调用.is_valid()
        if s.is_valid():
            s.save(teacher=self.request.user)
            # 分别是<class 'django.http.request.QueryDict'> <class 'rest_framework.utils.serializer_helpers.ReturnDict'>
            print(type(request.data), type(s.data))
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_object(pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return

    def get(self, request, pk):
        """
        :param request:
        :param pk:
        :return:
        """
        obj = self.get_object(pk=pk)
        if not obj:
            return Response(
                data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND
            )

        s = CourseSerializer(instance=obj)
        return Response(s.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        :param request:
        :param pk:
        :return:
        """
        obj = self.get_object(pk=pk)
        if not obj:
            return Response(
                data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND
            )

        s = CourseSerializer(instance=obj, data=request.data)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_200_OK)
        return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        :param request:
        :param pk:
        :return:
        """
        obj = self.get_object(pk=pk)
        if not obj:
            return Response(
                data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND
            )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""三、 通用类视图 Generic Class Based View"""


class GCourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class GCourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


"""四、 DRF的视图集viewsets"""


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
