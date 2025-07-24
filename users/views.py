from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserRegisterSerializer, UserSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Профиль пользователя",
        operation_description="Получает информацию о текущем авторизованном пользователе.",
        tags=["Профиль"]
    )
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_summary="Обновление профиля",
        operation_description="Обновляет профиль текущего пользователя.",
        tags=["Профиль"]
    )
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_summary="Частичное обновление профиля",
        operation_description="Частично обновляет профиль текущего пользователя.",
        tags=["Профиль"]
    )
)
class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Регистрация нового пользователя",
        operation_description="""
        Создаёт нового пользователя.

        Требуемые поля:
        - email
        - password
        """
    )
)
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
