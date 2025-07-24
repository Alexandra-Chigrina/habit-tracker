from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.services import send_telegram_message
from habits.tasks import send_habit_reminders
from habits.validators import validate_reward_and_related_habit, validate_pleasant_habit, validate_duration_limit, \
    validate_period

User = get_user_model()


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@mail.com", password="1234")
        self.other_user = User.objects.create(email="other@mail.com", password="1234")
        self.client.force_authenticate(user=self.user)
        self.own_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Пить воду",
            is_pleasant=False,
            period=1,
            duration=60,
            is_public=False
        )
        self.public_habit = Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="19:00",
            action="Прогулка",
            is_pleasant=False,
            period=1,
            duration=90,
            is_public=True
        )
        self.detail_url = reverse("habits:habits-detail", args=(self.own_habit.pk,))
        self.public_detail_url = reverse("habits:habits-detail", args=(self.public_habit.pk,))
        self.list_url = reverse("habits:habits-list")

    def test_list_own_habits(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Пить воду")

    def test_list_public_habits(self):
        response = self.client.get(self.list_url + "?is_public=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_own_habit(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_public_not_own_habit(self):
        response = self.client.get(self.public_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_habit(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.own_habit.pk).exists())

    def test_delete_other_user_habit(self):
        response = self.client.delete(self.public_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_habit(self):
        data = {
            "place": "Балкон",
            "time": "07:00",
            "action": "Зарядка",
            "is_pleasant": False,
            "period": 1,
            "duration": 90,
            "is_public": False
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(user=self.user).count(), 2)


class ValidatorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com")

    def _create_habit(self, is_pleasant=True):
        from habits.models import Habit
        return Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Чтение",
            is_pleasant=is_pleasant,
            period=1,
            duration=60,
            is_public=False
        )

    def test_both_reward_and_related_habit(self):
        related = self._create_habit(is_pleasant=True)

        with self.assertRaises(ValidationError) as e:
            validate_reward_and_related_habit({
                "reward": "Сладкое",
                "related_habit": related
            })
        self.assertIn("Нельзя указывать и вознаграждение, и связанную привычку", str(e.exception))

    def test_related_habit_must_be_pleasant(self):
        related = self._create_habit(is_pleasant=False)

        with self.assertRaises(ValidationError) as e:
            validate_reward_and_related_habit({
                "reward": None,
                "related_habit": related
            })
        self.assertIn("Связанная привычка должна быть помечена как приятная", str(e.exception))

    def test_pleasant_habit_must_not_have_reward_or_related(self):
        with self.assertRaises(ValidationError) as e:
            validate_pleasant_habit({
                "reward": "Сладкое",
                "related_habit": None,
                "is_pleasant": True
            })
        self.assertIn("Приятная привычка не может иметь награду или связанную привычку", str(e.exception))

        related = self._create_habit(is_pleasant=True)
        with self.assertRaises(ValidationError) as e:
            validate_pleasant_habit({
                "reward": None,
                "related_habit": related,
                "is_pleasant": True
            })
        self.assertIn("Приятная привычка не может иметь награду или связанную привычку", str(e.exception))

    def test_duration_must_not_exceed_120(self):
        with self.assertRaises(ValidationError) as e:
            validate_duration_limit({
                "duration": 150
            })
        self.assertIn("Время выполнения не может превышать 120 секунд", str(e.exception))

    def test_period_must_not_be_more_than_7_days(self):
        with self.assertRaises(ValidationError) as e:
            validate_period({
                "period": 8
            })
        self.assertIn("Периодичность должна быть от 1 до 7 дней", str(e.exception))


class ServiceTestCase(TestCase):

    @patch("habits.services.requests.get")
    def test_send_telegram_message_success(self, mock_get):
        mock_response = Mock()
        mock_response.ok = True
        mock_get.return_value = mock_response

        chat_id = "123456789"
        message = "Тестовое сообщение"

        send_telegram_message(chat_id, message)

        mock_get.assert_called_once()
        called_url = mock_get.call_args[0][0]
        called_params = mock_get.call_args[1]["params"]

        self.assertIn("sendMessage", called_url)
        self.assertEqual(called_params["chat_id"], chat_id)
        self.assertEqual(called_params["text"], message)

    @patch("habits.services.requests.get")
    def test_send_telegram_message_error(self, mock_get):
        mock_response = Mock()
        mock_response.ok = False
        mock_response.status_code = 400
        mock_response.text = "Bad Request: chat not found"
        mock_get.return_value = mock_response

        chat_id = "wrong_chat"
        message = "Ошибка"

        send_telegram_message(chat_id, message)

        mock_get.assert_called_once()
