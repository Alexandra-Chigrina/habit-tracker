from rest_framework.serializers import ValidationError


def validate_reward_and_related_habit(attrs):
    reward = attrs.get("reward")
    related_habit = attrs.get("related_habit")
    if reward and related_habit:
        raise ValidationError("Нельзя указывать и вознаграждение, и связанную привычку")
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError("Связанная привычка должна быть помечена как приятная")
    return attrs


def validate_pleasant_habit(attrs):
    if attrs.get("is_pleasant") and (attrs.get("related_habit") or attrs.get("reward")):
        raise ValidationError("Приятная привычка не может иметь награду или связанную привычку")
    return attrs


def validate_period(attrs):
    period = attrs.get("period", 1)
    if period > 7 or period < 1:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней")
    return attrs


def validate_duration_limit(attrs):
    if attrs.get("duration", 0) > 120:
        raise ValidationError("Время выполнения не может превышать 120 секунд")
    return attrs
