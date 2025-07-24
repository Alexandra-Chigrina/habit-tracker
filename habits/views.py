from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginators import CustomPagination
from habits.serializers import HabitSerializer


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
