from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from authentication.models import OTP, CustomUser, Location

User = get_user_model()


class TestCustomUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            date_of_birth="1990-01-01",
            gender="male",
            country="Egypt",
            phone_number="1234567890",
            auth_provider="email",
        )

    # Test user creation
    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpassword123"))
        self.assertEqual(self.user.gender, "male")
        self.assertEqual(self.user.country, "Egypt")

    # Test user's tokens
    def test_user_tokens_method(self):
        tokens = self.user.tokens()
        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)

    # Test user's group membership methods
    def test_user_group_membership_methods(self):
        # Test is_trainer method
        trainer_group, _ = Group.objects.get_or_create(name="trainers")
        self.user.groups.add(trainer_group)
        self.assertTrue(self.user.is_trainer())
        self.assertFalse(self.user.is_trainee())

        # Test is_trainee method
        self.user.groups.remove(trainer_group)
        trainee_group, _ = Group.objects.get_or_create(name="trainees")
        self.user.groups.add(trainee_group)
        self.assertTrue(self.user.is_trainee())
        self.assertFalse(self.user.is_trainer())

        # Test is_owner method
        owner_group, _ = Group.objects.get_or_create(name="branches")
        self.user.groups.add(owner_group)
        self.assertTrue(self.user.is_owner())

        # Test is_admin method
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)
        self.assertTrue(self.user.is_admin())

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), self.user.username + " ")

    # create_trainee
    def test_create_trainee(self):
        user = CustomUser.objects.create_trainee(
            email="ahmed@gmail.com", password="password"
        )
        self.assertEqual(user.email, "ahmed@gmail.com")
        self.assertTrue(user.check_password("password"))
        self.assertTrue(user.is_trainee())
        self.assertFalse(user.is_trainer())
        self.assertFalse(user.is_owner())
        self.assertFalse(user.is_admin())

    # create_trainer
    def test_create_trainer(self):
        user = CustomUser.objects.create_trainer(
            email="mohamed@gmail.com", password="password"
        )
        self.assertEqual(user.email, "mohamed@gmail.com")
        self.assertTrue(user.check_password("password"))
        self.assertTrue(user.is_trainer())
        self.assertFalse(user.is_trainee())
        self.assertFalse(user.is_owner())
        self.assertFalse(user.is_admin())

    # create_owner
    def test_create_owner(self):
        user = CustomUser.objects.create_owner(
            username="amar", email="amar@gmail.com", password="password"
        )
        self.assertEqual(user.email, "amar@gmail.com")
        self.assertTrue(user.check_password("password"))
        self.assertTrue(user.is_owner())
        self.assertFalse(user.is_trainee())
        self.assertFalse(user.is_trainer())
        self.assertFalse(user.is_admin())


class TestLocationModel(TestCase):
    def setUp(self):
        # Create a user instance to use for creating a Location
        self.user = CustomUser.objects.create_trainee(
            email="user@example.com", password="password"
        )
        self.user_content_type = ContentType.objects.get_for_model(CustomUser)

    def test_create_location_for_user(self):
        # Create a Location instance for the user created in setUp
        location = Location.objects.create(
            longitude=123.456789,
            latitude=98.765432,
            content_type=self.user_content_type,
            object_id=self.user.id,
        )
        # Verify the Location instance has been correctly associated with the user
        self.assertEqual(location.longitude, 123.456789)
        self.assertEqual(location.latitude, 98.765432)
        self.assertEqual(location.content_object, self.user)
        self.assertTrue(isinstance(location.content_object, CustomUser))
        self.assertEqual(location.content_object.email, "user@example.com")

    def test_location_string_representation(self):
        # Create a Location instance
        location = Location.objects.create(
            longitude=123.456789,
            latitude=98.765432,
            content_type=self.user_content_type,
            object_id=self.user.id,
        )

        # Verify the string representation
        expected_string = f"{location.longitude}, {location.latitude} - {location.content_object}'s Location"
        self.assertEqual(str(location), expected_string)


class OTPModelTests(TestCase):
    def setUp(self):
        self.otp_instance = OTP.objects.create(
            email="user@example.com",
            otp=1234,
            validity=timezone.now() + timedelta(minutes=5),
            verified=False,
        )

    # Test OTP creation
    def test_otp_creation(self):
        self.assertEqual(self.otp_instance.email, "user@example.com")
        self.assertEqual(self.otp_instance.otp, 1234)
        self.assertFalse(self.otp_instance.verified)
        self.assertTrue(self.otp_instance.validity > timezone.now())

    # Test OTP string representation
    def test_otp_string_representation(self):
        self.assertEqual(str(self.otp_instance), "user@example.com")
