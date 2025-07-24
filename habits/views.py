from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import CustomPagination
from habits.serializers import HabitSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="Список привычек",
        operation_description="""
        Возвращает список привычек:
        - если передан параметр `is_public=true`, возвращаются все публичные привычки;
        - иначе возвращаются только привычки текущего пользователя.
        """,
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Получить привычку по ID",
        operation_description="Возвращает одну привычку. Доступна только владельцу привычки.",
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Создать привычку",
        operation_description="Создает новую привычку, привязанную к текущему пользователю.",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_summary="Обновить привычку",
        operation_description="Полное обновление привычки. Доступно только владельцу.",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Частично обновить привычку",
        operation_description="Частичное обновление привычки. Доступно только владельцу.",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Удалить привычку", operation_description="Удаляет привычку. Доступно только владельцу."
    ),
)
class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Для просмотра публичных привычек отправляется GET-запрос с параметром is_public=True"""
        if self.action == "list":
            is_public = self.request.query_params.get("is_public")
            if is_public and is_public.lower() == "true":
                return Habit.objects.filter(is_public=True)
            return Habit.objects.filter(user=self.request.user)
        return Habit.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("Вы не можете просматривать, редактировать или удалять чужие привычки.")
        return obj
