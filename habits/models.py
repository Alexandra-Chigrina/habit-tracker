from django.db import models

from config import settings


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место", help_text="Укажите место")
    time = models.TimeField(verbose_name="Время", help_text="Укажите время")
    action = models.CharField(max_length=255, verbose_name="Действие", help_text="Укажите действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки", help_text="Укажите, является ли привычка приятной"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_pleasant": True},
        related_name="habits",
        verbose_name="Связанная привычка",
    )
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение", help_text="Укажите вознаграждение"
    )
    period = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность", help_text="Укажите периодичность в днях"
    )
    duration = models.PositiveIntegerField(
        verbose_name="Время на выполнение", help_text="Укажите время на выполнение привычки в секундах"
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Укажите, можно ли публиковать привычку в общий доступ",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.action} в {self.time.strftime('%H:%M')} в {self.place}"
