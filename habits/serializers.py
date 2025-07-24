from rest_framework import serializers

from habits.models import Habit
from habits.validators import (
    validate_duration_limit,
    validate_period,
    validate_pleasant_habit,
    validate_reward_and_related_habit
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, attrs):
        attrs = validate_reward_and_related_habit(attrs)
        attrs = validate_pleasant_habit(attrs)
        attrs = validate_duration_limit(attrs)
        attrs = validate_period(attrs)
        return attrs
