from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "user", "is_pleasant", "is_public")
    list_filter = ("user",)
    search_fields = ("action",)
