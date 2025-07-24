from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_telegram_message
from users.models import User


@shared_task
def send_habit_reminders():
    """Отправляет напоминание пользователям о привычках, запланированных на текущее время"""
    current_time = timezone.localtime().time().strftime("%H:%M")
    users = User.objects.filter(tg_chat_id__isnull=False)
    for user in users:
        habits = Habit.objects.filter(time=current_time, user=user)
        for habit in habits:
            message = f"Напоминание: {habit.action} в {habit.time.strftime('%H:%M')}"
            send_telegram_message(user.tg_chat_id, message)
            print(f"[{user.email}] Отправлено напоминание: {habit.action} в {habit.time.strftime('%H:%M')}")
