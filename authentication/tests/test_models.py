from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from authentication.models import OTP, Location

User = get_user_model()


class TestUser(TestCase):
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
        self.trainee = User.objects.create_trainee(
            email="trainee@example.com",
            password="password",
        )
        self.trainer = User.objects.create_trainer(
            email="trainer@example.com",
            password="password",
        )
        self.owner = User.objects.create_owner(
            username="owner",
            email="owner@example.com",
            password="password",
        )
        self.admin = User.objects.create_admin(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.superuser = User.objects.create_superuser(
            username="superuser",
            email="superuser@example.com",
            password="password",
        )

    # Test Email Filed must be set
    def test_email_field_must_be_set(self):
        with self.assertRaises(ValueError) as cm:
            User.objects.create_user(
                username="testuser",
                email="",
                password="testpassword123",
                date_of_birth="1990-01-01",
            )
        self.assertEqual(str(cm.exception), "The Email field must be set")

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
        admin_group, _ = Group.objects.get_or_create(name="admins")
        self.user.groups.add(admin_group)
        self.assertTrue(self.user.is_admin())

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), self.user.username + " ")

    # create_trainee
    def test_create_trainee(self):
        self.assertEqual(self.trainee.email, "trainee@example.com")
        self.assertTrue(self.trainee.check_password("password"))
        self.assertTrue(self.trainee.is_trainee())
        self.assertFalse(self.trainee.is_trainer())
        self.assertFalse(self.trainee.is_owner())
        self.assertFalse(self.trainee.is_admin())

    # create_trainer
    def test_create_trainer(self):
        self.assertEqual(self.trainer.email, "trainer@example.com")
        self.assertTrue(self.trainer.check_password("password"))
        self.assertTrue(self.trainer.is_trainer())
        self.assertFalse(self.trainer.is_trainee())
        self.assertFalse(self.trainer.is_owner())
        self.assertFalse(self.trainer.is_admin())

    # create_owner
    def test_create_owner(self):
        self.assertEqual(self.owner.email, "owner@example.com")
        self.assertTrue(self.owner.check_password("password"))
        self.assertTrue(self.owner.is_owner())
        self.assertFalse(self.owner.is_trainee())
        self.assertFalse(self.owner.is_trainer())
        self.assertFalse(self.owner.is_admin())

    # create_admin
    def test_create_admin(self):
        self.assertEqual(self.admin.email, "admin@example.com")
        self.assertTrue(self.admin.check_password("password"))
        self.assertTrue(self.admin.is_admin())
        self.assertFalse(self.admin.is_trainee())
        self.assertFalse(self.admin.is_trainer())
        self.assertFalse(self.admin.is_owner())

    # create_superuser
    def test_create_superuser(self):
        self.assertEqual(self.superuser.email, "superuser@example.com")
        self.assertTrue(self.superuser.check_password("password"))
        self.assertTrue(self.superuser.is_admin())
        self.assertFalse(self.superuser.is_trainee())
        self.assertFalse(self.superuser.is_trainer())
        self.assertFalse(self.superuser.is_owner())
    
    
    # Test check group function
    def test_check_group(self):
        # Test when the user is not a member of the group
        self.assertFalse(self.user.check_group("trainee"))

        # Add the user to the group
        trainee_group, _ = Group.objects.get_or_create(name="trainees")
        self.user.join_group("trainees")

        # Test when the user is a member of the group
        self.assertTrue(self.user.check_group("trainee"))

    # Test join group function
    def test_join_group(self):
        # Test joining a group
        self.assertFalse(self.user.check_group("trainee"))

        self.user.join_group("trainees")

        self.assertTrue(self.user.check_group("trainee"))


class TestLocationModel(TestCase):
    def setUp(self):
        # Create a user instance to use for creating a Location
        self.user = User.objects.create_trainee(
            email="user@example.com", password="password"
        )
        self.user_content_type = ContentType.objects.get_for_model(User)

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
        self.assertTrue(isinstance(location.content_object, User))
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
