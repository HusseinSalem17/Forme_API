from django.test import TestCase
from django.contrib.auth.models import Group
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from authentication.admin import CustomUserAdmin
from authentication.models import CustomUser

User = get_user_model()


class CustomUserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = CustomUserAdmin(User, self.site)

    def test_get_group(self):
        # Create a custom user with groups
        user = CustomUser.objects.create(username="testuser")
        group1 = Group.objects.create(name="Group 1")
        group2 = Group.objects.create(name="Group 2")
        user.groups.set([group1, group2])

        # Call the get_group method
        result = self.admin.get_group(user)

        # Check if the result is correct
        self.assertEqual(result, "Group 1, Group 2")
