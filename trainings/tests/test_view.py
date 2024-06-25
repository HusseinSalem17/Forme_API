from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from trainings.models import Program, Trainer

User = get_user_model()


class ProgramsTrainerListViewTests(APITestCase):
    def setUp(self):
        # Create a user and a trainer
        self.user = User.objects.create_trainee(
            email="testuser@example.com",
            password="password",
        )
        self.trainer = User.objects.create_trainer(
            email="testtrainer@example.com",
            password="password",
        )
        self.trainer = Trainer.objects.create(user=self.trainer)
        self.program = Program.objects.create(title="test program", trainer=self.trainer)
        self.url = reverse("programs_trainer_list")

    def test_get_trainers_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        print('response.data', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))  # Expecting list of trainers

    # def test_get_no_trainers_found(self):
    #     # Delete all trainers to simulate no trainers found
    #     Trainer.objects.all().delete()
    #     self.client.force_authenticate(user=self.user)
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_get_trainers_unauthorized(self):
    #     # Attempt to access the endpoint without authentication
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # # Additional tests for edge cases and error handling can be added here
