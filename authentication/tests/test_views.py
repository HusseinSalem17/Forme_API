from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from authentication.models import OTP, Location
from django.contrib.auth import get_user_model

from authentication.serializers import RegisterSerializer
from django.contrib.contenttypes.models import ContentType

from trainings.models import Trainee, Trainer


User = get_user_model()


class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.request_otp_url = reverse("request_otp")
        self.verify_otp_url = reverse("verify_otp_view")
        self.register_url = reverse("register")

    def test_user_registration_success(self):
        # Request OTP
        data = {"email": "newuser@test.com", "user_type": "trainer"}
        response = self.client.post(self.request_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        otp = OTP.objects.get(email="newuser@test.com").otp

        # Verify OTP
        data = {"email": "newuser@test.com", "otp": otp}
        response = self.client.post(self.verify_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Register
        data = {
            "email": "newuser@test.com",
            "password": "newpass",
            "user_type": "trainer",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_failure(self):
        # Request OTP with invalid user type
        data = {"email": "newuser@test.com", "user_type": "invalid_user_type"}
        response = self.client.post(self.request_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify OTP with wrong OTP
        data = {"email": "newuser@test.com", "otp": "1234"}
        response = self.client.post(self.verify_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Register with invalid user type
        data = {
            "email": "newuser@test.com",
            "password": "newpass",
            "user_type": "invalid_user_type",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(RegisterSerializer, "save", side_effect=Exception("Test exception"))
    def test_user_registration_exception(self, save_mock):
        # Request OTP
        data = {"email": "newuser@test.com", "user_type": "trainer"}
        response = self.client.post(self.request_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        otp = OTP.objects.get(email="newuser@test.com").otp

        # Verify OTP
        data = {"email": "newuser@test.com", "otp": otp}
        response = self.client.post(self.verify_otp_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Register with exception
        data = {
            "email": "newuser@test.com",
            "password": "newpass",
            "user_type": "trainer",
        }
        response = self.client.post(self.register_url, data)
        print("here response 1", response.data)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_trainee(
            email="testuser@test.com", password="testpass"
        )
        self.login_url = reverse("login")

    def test_login_success(self):
        data = {
            "email": "testuser@test.com",
            "password": "testpass",
            "user_type": "trainee",
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self):
        data = {"email": "testuser@test.com", "password": "wrongpass"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LocatinoViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="testuser@test.com", password="testpass")
        self.location = Location.objects.create(
            latitude=23.456,
            longitude=45.678,
            content_type=ContentType.objects.get_for_model(self.user),
            object_id=self.user.id,
        )
        self.location_url = reverse("location")

    def test_get_location_failure(self):
        response = self.client.get(self.location_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_location_success(self):
        self.client.force_authenticate(user=self.user)
        new_location_data = {"longitude": "24.123000", "latitude": "46.789000"}
        response = self.client.patch(self.location_url, new_location_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["latitude"], new_location_data["latitude"])
        self.assertEqual(response.data["longitude"], new_location_data["longitude"])

    def test_get_location_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.location_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["latitude"], "23.456000")
        self.assertEqual(response.data["longitude"], "45.678000")

    def test_patch_location_failure(self):
        new_location_data = {"longitude": 24.123000, "latitude": 46.789000}
        response = self.client.patch(self.location_url, new_location_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CompleteProfileTraineeViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_trainee(
            email="testuser@test.com",
            password="testpass",
        )
        Trainee.objects.create(user=self.user)
        self.complete_profile_url = reverse("complete_profile_trainee")

    def test_complete_profile_success(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "username": "newusername",
            "country": "newcountry",
            "gender": "male",
        }
        response = self.client.patch(self.complete_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_profile_failure_not_trainee(self):
        user = User.objects.create_user(
            username="testuser", email="testuser2@test.com", password="testpass"
        )
        self.client.force_authenticate(user=user)
        data = {
            "username": "newusername",
            "country": "newcountry",
            "gender": "female",
        }
        response = self.client.patch(self.complete_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_complete_profile_failure_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "username": "",
            "country": "newcountry",
            "gender": "newgender",
        }
        response = self.client.patch(self.complete_profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CompleteProfileTrainerViewTest(APITestCase):
    def setUp(self):
        self.complete_profile_url = reverse("complete_profile_trainer")
        self.user = User.objects.create_trainer(
            email="testuser@test.com", password="testpass"
        )
        self.trainer = Trainer.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_complete_profile_success(self):
        data = {
            "user": {
                "username": "newusername",
                "date_of_birth": "1990-01-01",
                "country": "USA",
                "phone_number": "1234567890",
                "gender": "male",
            },
            "sport_field": "Football",
        }
        response = self.client.patch(self.complete_profile_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], data["user"]["username"])
        self.assertEqual(response.data["sport_field"], data["sport_field"])

    def test_complete_profile_failure_not_trainer(self):
        self.trainer.delete()
        data = {
            "user": {
                "username": "newusername",
                "date_of_birth": "1990-01-01",
                "country": "USA",
                "phone_number": "1234567890",
                "gender": "male",
            },
            "sport_field": "Football",
        }
        response = self.client.patch(self.complete_profile_url, data, format="json")
        print("here response1", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_complete_profile_failure_invalid_data(self):
        data = {
            "user": {
                "username": "",
                "date_of_birth": "1990-01-01",
                "country": "USA",
                "phone_number": "1234567890",
                "gender": "male",
            },
            "sport_field": "Football",
        }
        response = self.client.patch(self.complete_profile_url, data, format="json")
        print("here response2", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutAPIViewTest(APITestCase):
    def setUp(self):
        self.logout_url = reverse("logout")
        self.user = User.objects.create_trainee(
            email="testuser@test.com", password="testpass"
        )
        Trainee.objects.create(user=self.user)

    def test_logout_success(self):
        self.client.force_authenticate(user=self.user)
        refresh = self.user.tokens()["refresh"]
        data = {"refresh": str(refresh)}
        response = self.client.post(self.logout_url, data)
        print("here response", response.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_unauthenticated(self):
        self.client.logout()
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteAccountViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_trainee(
            email="testuser@test.com",
            password="testpass",
        )
        Trainee.objects.create(user=self.user)
        self.token = self.user.tokens()["access"]
        self.delete_account_url = reverse("delete_account")

    def test_delete_account_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "User deleted successfully")

    def test_delete_account_unauthorized(self):
        response = self.client.delete(self.delete_account_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdatePreferenceTraineeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_trainee(
            email="testuser@test.com", password="testpass"
        )
        Trainee.objects.create(user=self.user)
        self.update_preference_url = reverse("update_preference_trainee")

    def test_update_preference_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "user": {
                "date_of_birth": "1990-01-01",
            },
            "height": 180,
            "weight": 80,
            "fitness_goals": "lose_weight",
            "current_physical_level": "beginner",
        }
        response = self.client.put(self.update_preference_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Preference Updated successfully!",
        )

    def test_update_preference_failure_not_trainee(self):
        user = User.objects.create_user(
            username="testuser",
            email="user@test.com",
            password="testpass",
        )
        self.client.force_authenticate(user=user)
        data = {
            "user": {
                "date_of_birth": "1990-01-01",
            },
            "height": 180,
            "weight": 80,
            "fitness_goals": "lose_weight",
            "current_physical_level": "beginner",
        }
        response = self.client.put(self.update_preference_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_preference_failure_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "user": {
                "date_of_birth": "1990-01-01",
            },
            "height": 180,
            "weight": 80,
            "fitness_goals": "lose_weight",
            "current_physical_level": "invalid_physical_level",
        }
        response = self.client.put(self.update_preference_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdatePreferenceTrainerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_trainer(
            email="testuser@test.com",
            password="testpass",
        )
        Trainer.objects.create(user=self.user)
        self.update_preference_url = reverse("update_preference_trainer")

    def test_update_preference_success(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "bio": "new bio",
            "exp_injuries": False,
            "physical_disabilities": True,
            "languages": ["English", "French"],
            "facebook_url": "https://web.facebook.com/reel/1118788825939824",
            "instagram_url": "https://www.instagram.com/reel/1118788825939824",
            "youtube_url": "https://www.youtube.com/watch?v=sXXIPtDKMMk",
        }
        response = self.client.put(self.update_preference_url, data, format="json")
        print("here response0", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "Preference Updated successfully!",
        )

    def test_update_preference_failure_not_trainer(self):
        user = User.objects.create_user(
            username="testuser",
            email="user@test.com",
            password="testpass",
        )
        self.client.force_authenticate(user=user)
        data = {
            "bio": "new bio",
            "exp_injuries": False,
            "physical_disabilities": True,
            "languages": ["English", "French"],
            "facebook_url": "https://web.facebook.com/reel/1118788825939824",
            "instagram_url": "https://www.instagram.com/reel/1118788825939824",
            "youtube_url": "https://www.youtube.com/watch?v=sXXIPtDKMMk",
        }
        response = self.client.put(self.update_preference_url, data, format="json")
        print("here response1", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_preference_failure_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "bio": "new bio",
            "exp_injuries": "Hi",
            "physical_disabilities": True,
            "languages": ["English", "French"],
            "facebook_url": "https://web.facebook.com/reel/1118788825939824",
            "instagram_url": "https://www.instagram.com/reel/1118788825939824",
            "youtube_url": "https://www.youtube.com/watch?v=sXXIPtDKMMk",
        }
        response = self.client.put(self.update_preference_url, data, format="json")
        print("here response2", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ForgetPasswordViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_trainee(
            email="testuser@test.com",
            password="testpass",
        )
        Trainee.objects.create(user=self.user)
        self.verify_otp_url = reverse("verify_otp_view")
        self.forget_password_url = reverse("forget_password")
        self.set_new_password_url = reverse("set_new_password")

    def test_forget_password_success(self):
        # Forget Password
        data = {"email": "testuser@test.com"}
        response = self.client.post(self.forget_password_url, data)
        print("here response12", response.data)
        print("status code", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "We have sent otp to your email!")

        # Verify OTP
        otp = OTP.objects.get(email="testuser@test.com").otp
        data = {"email": "testuser@test.com", "otp": otp}
        response = self.client.post(self.verify_otp_url, data)
        print("here response13", response.data)
        print("status code", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "OTP verified successfully!")

        # Set New Password
        data = {"email": "testuser@test.com", "new_password": "newpass"}
        response = self.client.put(self.set_new_password_url, data)
        print("here response14", response.data)
        print("status code", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password updated successfully!")

    def test_forget_password_failure(self):
        # Forget Password with invalid email
        data = {"email": "user@test.com"}
        response = self.client.post(self.forget_password_url, data)
        print('here response15', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify OTP with invalid email
        data = {"email": "user@test.com", "otp": "1234"}
        response = self.client.post(self.verify_otp_url, data)
        print('here response16', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Set New Password with invalid email
        data = {"email": "user@test.com", "new_password": "newpass"}
        response = self.client.put(self.set_new_password_url, data)
        print('here response17', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ResetPasswordViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_trainee(
            email="testuser@test.com",
            password="testpass",
        )
        Trainee.objects.create(user=self.user)
        self.reset_password_url = reverse("reset_password_view")

    def test_reset_password_success(self):
        self.client.force_authenticate(user=self.user)
        data = {"old_password": "testpass", "new_password": "newpass"}
        response = self.client.put(self.reset_password_url, data)
        print('here response18', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password updated successfully!")

    def test_reset_password_failure(self):
        self.client.force_authenticate(user=self.user)
        data = {"old_password": "wrongpass", "new_password": "newpass"}
        response = self.client.put(self.reset_password_url, data)
        print('here response19', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Old password is incorrect")

    def test_reset_password_unauthenticated(self):
        data = {"old_password": "testpass", "new_password": "newpass"}
        response = self.client.put(self.reset_password_url, data)
        print('here response20', response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Authentication credentials were not provided."
        )