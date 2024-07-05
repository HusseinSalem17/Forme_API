from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from clubs.models import (
    Attendance,
    BranchGallery,
    BranchMember,
    BranchTrainer,
    Club,
    Branch,
    MemberSubscription,
    NewTrainer,
    Subscription,
    SubscriptionPlan,
)
from trainings.models import Review, Trainee, Trainer
from django.contrib.contenttypes.models import ContentType


User = get_user_model()


# class AttendanceUpdateViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )

#         self.user_trainee = User.objects.create_trainee(
#             email="trainee@example.com",
#             password="password123",
#         )
#         self.trainee = Trainee.objects.create(
#             user=self.user_trainee,
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.member = BranchMember.objects.create(
#             trainee=self.trainee,
#             branch=self.branch,
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             target_gender="male",
#             min_age=18,
#             max_age=40,
#             branch=self.branch,
#         )
#         self.subscription_plan = SubscriptionPlan.objects.get(
#             subscription=self.subscription,
#             duration=2,
#         )
#         self.member_subscription = MemberSubscription.objects.create(
#             subscription=self.subscription,
#             subscription_plan=self.subscription_plan,
#             member=self.member,
#             state="active",
#             start_date="2024-06-23",
#             end_date="2024-06-28",
#         )
#         self.attendance = self.member_subscription.member_attendance.first()
#         self.url = reverse(
#             "attendance_update", kwargs={"attendance_id": self.attendance.id}
#         )

#     def test_attendance_update_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         data = {
#             "is_present": True,
#             "date": "10:00:00",
#         }
#         response = self.client.put(self.url, data, format="json")
#         print("attendance response.data", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(Attendance.objects.get(id=self.attendance.id).is_present)

#     def test_attendance_update_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         data = {
#             "is_present": True,
#             "date": "10:00:00",
#         }
#         response = self.client.put(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_attendance_update_without_authentication(self):
#         data = {
#             "is_present": True,
#             "date": "10:00:00",
#         }
#         response = self.client.put(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_attendance_update_invalid_data(self):
#         self.client.force_authenticate(user=self.user_owner)
#         data = {
#             "is_present": True,
#             "date": "10:00:00",
#         }
#         response = self.client.put(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(Attendance.objects.get(id=self.attendance.id).is_present)

#     def test_attendance_update_nonexistent_attendance(self):
#         self.client.force_authenticate(user=self.user_owner)
#         self.attendance.delete()
#         data = {
#             "is_present": True,
#             "date": "10:00:00",
#         }
#         response = self.client.put(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class BranchDeleteViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.url = reverse("branch_delete")

#     def test_branch_delete_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "Branch deleted successfully")
#         self.assertFalse(Branch.objects.filter(id=self.branch.id).exists())

#     def test_branch_delete_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_branch_delete_without_authentication(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_branch_delete_nonexistent_branch(self):
#         self.client.force_authenticate(user=self.user_owner)
#         self.branch.delete()  # Delete the branch to simulate a nonexistent branch scenario
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
#         self.assertIn("error", response.data)


class BranchDetailViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("branch_detail")
        self.user_non_owner = User.objects.create_user(
            username="nonowneruser",
            email="nonowner@example.com",
            password="password123",
        )
        self.user_owner = User.objects.create_owner(
            username="testuser",
            email="test@example.com",
            password="password123",
        )
        self.club = Club.objects.create(
            property_name="Test Club", sport_field="Football"
        )
        self.branch = Branch.objects.create(
            owner=self.user_owner,
            club=self.club,
            address="123 Test St",
            details="Test details",
        )

    def test_branch_detail_success(self):
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(self.url)
        # print('here detail response.data', response.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["address"], self.branch.address)
        # self.assertEqual(response.data["details"], self.branch.details)

#     def test_branch_detail_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.get(self.url)
#         print("response.data Nowww", response.data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_branch_detail_without_authentication(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class BranchRegisterViewTests(APITestCase):
#     def setUp(self):
#         self.url = reverse("branch_register")
#         self.user_data = {
#             "username": "testuser",
#             "email": "test@example.com",
#             "password": "password123",
#             "confirm_password": "password123",
#             "phone_number": "1234567890",
#         }
#         self.club_data = {"property_name": "Test Club", "sport_field": "Football"}
#         self.branch_data = {"address": "123 Test St", "details": "Test details"}

#     def test_register_branch_success(self):
#         data = {
#             "owner": self.user_data,
#             "club": self.club_data,
#             "address": self.branch_data["address"],
#             "details": self.branch_data["details"],
#         }
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn("message", response.data)
#         self.assertEqual(
#             response.data["message"],
#             "Branch registered successfully, we will contact you soon",
#         )
#         self.assertTrue(Club.objects.exists())
#         self.assertTrue(Branch.objects.exists())
#         self.assertTrue(
#             get_user_model().objects.filter(email=self.user_data["email"]).exists()
#         )

#     def test_register_branch_with_existing_email(self):
#         User.objects.create_owner(
#             username="test",
#             email="test@example.com",
#             password="password123",
#         )
#         data = {
#             "owner": self.user_data,
#             "club": self.club_data,
#             "address": self.branch_data["address"],
#             "details": self.branch_data["details"],
#         }
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "user with this email already exists.")

#     def test_register_branch_with_invalid_data(self):
#         data = {
#             "owner": {},  # Empty owner data
#             "club": self.club_data,
#             "address": self.branch_data["address"],
#             "details": self.branch_data["details"],
#         }
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)


# class BranchLoginViewTests(APITestCase):
#     def setUp(self):
#         self.url = reverse("branch_login")
#         self.user_credentials = {
#             "email": "test@example.com",
#             "password": "password123",
#         }
#         self.user = User.objects.create_owner(
#             username="test",
#             email="test@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#             is_verified=True,
#         )

#     def test_login_success(self):
#         response = self.client.post(self.url, self.user_credentials, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("access", response.data)
#         self.assertIn("refresh", response.data)

#     def test_login_with_invalid_credentials(self):
#         wrong_credentials = {
#             "email": "test@example.com",
#             "password": "wrongpassword",
#         }
#         response = self.client.post(self.url, wrong_credentials, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)

#     def test_login_with_missing_fields(self):
#         incomplete_credentials = {
#             "email": "test@example.com",
#         }
#         response = self.client.post(self.url, incomplete_credentials, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)


# class BranchUpdateViewTests(APITestCase):
#     def setUp(self):
#         self.url = reverse("branch_update")
#         self.user = User.objects.create_owner(
#             username="testuser",
#             email="test@example.com",
#             password="password123",
#         )
#         self.client.force_authenticate(user=self.user)
#         self.club = Club.objects.create(
#             property_name="Test Club", sport_field="Football"
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.update_data = {
#             "owner": {
#                 "username": "updateduser",
#                 "date_of_birth": "1990-01-02",
#                 "gender": "female",
#                 "country": "USA",
#                 "profile_picture": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=",
#                 "phone_number": "0987654321",
#             },
#             "club": {
#                 "property_name": "Updated Club",
#                 "sport_field": "Basketball",
#             },
#             "working_hours": [
#                 {
#                     "day": "Monday",
#                     "is_open": True,
#                     "day_time": [
#                         {
#                             "from_time": "08:00:00",
#                             "to_time": "16:00:00",
#                         }
#                     ],
#                 }
#             ],
#             "address": "456 Updated St",
#             "details": "Updated details",
#         }

#     def test_branch_update_success(self):
#         print('here is data', self.update_data)
#         response = self.client.patch(self.url, self.update_data, format="json")
#         print("response.data", response.data)
#         branch = Branch.objects.get(id=self.branch.id)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(branch.address, self.update_data["address"])
        # self.assertEqual(branch.details, self.update_data["details"])

    # def test_branch_update_unauthorized(self):
    #     self.client.logout()
    #     response = self.client.patch(self.url, self.update_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_branch_update_with_invalid_data(self):
    #     invalid_data = self.update_data.copy()
    #     invalid_data["address"] = ""  # Invalid address
    #     response = self.client.patch(self.url, invalid_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_branch_update_nonexistent_branch(self):
    #     self.branch.delete()  # Delete the branch to simulate non-existence
    #     response = self.client.patch(self.url, self.update_data, format="json")
    #     print("response.data here", response.data)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class ExistingTrainerAddViewTests(APITestCase):
#     def setUp(self):
#         # Create a user who will act as a branch owner
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         # Create a club
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         # Create a branch under the club
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         # Create a trainer user
#         self.trainer_user = User.objects.create_trainer(
#             email="trainer@example.com",
#             password="password123",
#         )
#         # Create a trainer profile
#         self.trainer = Trainer.objects.create(
#             user=self.trainer_user,
#         )
#         # URL for adding an existing trainer to a branch
#         self.url = reverse("existing_trainer_add")

#     def test_add_existing_trainer_success(self):
#         # Authenticate as the branch owner
#         self.client.force_authenticate(user=self.user_owner)
#         # Prepare data for adding an existing trainer
#         data = {
#             "trainer_slug": self.trainer.slug,
#         }
#         # Send POST request to add an existing trainer
#         response = self.client.post(self.url, data)
#         print("now response.data", response.data)
#         # Assert that the trainer was added successfully
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(BranchTrainer.objects.count(), 1)
#         self.assertEqual(BranchTrainer.objects.first().trainer, self.trainer)

#         # check can't add the same trainer again
#         response = self.client.post(self.url, data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(
#             response.data["error"], "Trainer already exists in this branch"
#         )
#         self.assertEqual(BranchTrainer.objects.count(), 1)

#     def test_add_existing_trainer_unauthorized(self):
#         # Authenticate as a user who is not the branch owner
#         self.client.force_authenticate(user=self.trainer_user)
#         # Prepare data for adding an existing trainer
#         data = {
#             "trainer_slug": self.trainer.slug,
#         }
#         # Send POST request to add an existing trainer
#         response = self.client.post(self.url, data)
#         print("now 1response.data", response.data)
#         # Assert that the request was unauthorized
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_add_existing_trainer_without_authentication(self):
#         # Prepare data for adding an existing trainer
#         data = {
#             "trainer_slug": self.trainer.slug,
#         }
#         # Send POST request to add an existing trainer without authentication
#         response = self.client.post(self.url, data)
#         print("now 2response.data", response.data)
#         print("now 2response.status_code", response.status_code)
#         # Assert that authentication is required
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_add_existing_trainer_invalid_data(self):
#         # Authenticate as the branch owner
#         self.client.force_authenticate(user=self.user_owner)
#         # Prepare invalid data (missing trainer_id)
#         data = {
#             "trainer_slug": self.branch.id,
#         }
#         # Send POST request with invalid data
#         response = self.client.post(self.url, data)
#         # Assert that the request was bad due to invalid data
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class ExistingTrainerDeleteViewTests(APITestCase):
#     def setUp(self):
#         # Create a user with owner permissions
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         # Create a non-owner user
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )
#         # Create a club
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         # Create a branch under the club
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         # Create a trainer user
#         self.trainer_user = User.objects.create_trainer(
#             email="trainer@example.com",
#             password="password123",
#         )
#         # Create a trainer profile
#         self.trainer = Trainer.objects.create(
#             user=self.trainer_user,
#         )
#         # Add the trainer to the branch
#         self.branch_trainer = BranchTrainer.objects.create(
#             branch=self.branch,
#             trainer=self.trainer,
#         )
#         # URL for deleting a branch trainer
#         self.url = reverse(
#             "existing_trainer_delete",
#             kwargs={"branch_trainer_id": self.branch_trainer.id},
#         )

#     def test_existing_trainer_delete_success(self):
#         # Authenticate as the owner
#         self.client.force_authenticate(user=self.user_owner)
#         # Attempt to delete the branch trainer
#         response = self.client.delete(self.url)
#         print("here now response.data", response.data)
#         # Assert the deletion was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(
#             response.data["message"], "Branch trainer deleted successfully"
#         )
#         # Assert the branch trainer no longer exists
#         self.assertFalse(
#             BranchTrainer.objects.filter(id=self.branch_trainer.id).exists()
#         )

#     def test_existing_trainer_delete_unauthorized(self):
#         # Authenticate as a non-owner
#         self.client.force_authenticate(user=self.user_non_owner)
#         # Attempt to delete the branch trainer
#         response = self.client.delete(self.url)
#         print("here now response.data", response.data)
#         # Assert the request was forbidden
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_existing_trainer_delete_not_found(self):
#         # Authenticate as the owner
#         self.client.force_authenticate(user=self.user_owner)
#         # Change the URL to an invalid branch trainer ID
#         invalid_url = reverse(
#             "existing_trainer_delete", kwargs={"branch_trainer_id": 999}
#         )
#         # Attempt to delete a non-existent branch trainer
#         response = self.client.delete(invalid_url)
#         print("here now response.data", response.data)
#         # Assert the branch trainer was not found
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Branch trainer not found")

#     def test_existing_trainer_delete_without_authentication(self):
#         # Attempt to delete the branch trainer without authentication
#         response = self.client.delete(self.url)
#         # Assert the request was unauthorized
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class BranchGalleriesViewTests(APITestCase):
#     def setUp(self):
#         # Create a user and authenticate
#         self.user = User.objects.create_owner(
#             username="testuser",
#             email="test@example.com",
#             password="testpassword",
#         )
#         # Authenticate as the branch owner
#         self.client.force_authenticate(user=self.user)
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.add_url = reverse("add_branch_gallery")
#         self.gallery_data = {
#             "gallery": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=",
#         }

#         # URL for the BranchGalleriesView
#         self.url = reverse("branch_galleries")

#     def test_get_branch_galleries_success(self):
#         # Add a gallery to the branch
#         self.client.post(self.add_url, self.gallery_data, format="json")
#         # Get the galleries for the branch
#         response = self.client.get(self.url)
#         print("nowww response.data", response.data)
#         # Assert the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Assert the response contains the gallery
#         self.assertEqual(len(response.data), 1)

#     def test_get_branch_galleries_no_branch(self):
#         # Test response when the user has no branch
#         self.branch.delete()  # Delete the branch to simulate no branch scenario
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Branch does not exist")

#     def test_get_branch_galleries_no_galleries(self):
#         # Test response when there are no galleries for the branch
#         BranchGallery.objects.all().delete()  # Delete all galleries
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 0)  # Expect empty list in response

#     def test_get_branch_galleries_unauthenticated(self):
#         # Test response when the user is not authenticated
#         self.client.logout()  # Log out to simulate unauthenticated request
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class BranchGalleryAddViewTests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_owner(
#             username="testuser",
#             email="test@example.com",
#             password="testpassword",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.url = reverse("add_branch_gallery")
#         self.gallery_data = {
#             "gallery": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=",
#         }

#     def test_gallery_add_success(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.post(self.url, self.gallery_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(BranchGallery.objects.filter(branch=self.branch).exists())

#     def test_gallery_add_without_authentication(self):
#         response = self.client.post(self.url, self.gallery_data, format="multipart")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_gallery_add_with_invalid_data(self):
#         self.client.force_authenticate(user=self.user)
#         invalid_data = {"description": "Missing image"}
#         response = self.client.post(self.url, invalid_data, format="multipart")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_gallery_add_for_non_owner_user(self):
#         non_owner_user = User.objects.create_user(
#             username="nonowner", email="nonowner@example.com", password="password123"
#         )
#         self.client.force_authenticate(user=non_owner_user)
#         response = self.client.post(self.url, self.gallery_data, format="multipart")
#         self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertFalse(BranchGallery.objects.filter(branch=self.branch).exists())


# class BranchGalleryDeleteViewTests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_owner(
#             username="testuser", email="test@example.com", password="testpassword"
#         )
#         self.client.force_authenticate(user=self.user)
#         self.club = Club.objects.create(
#             property_name="Test Club", sport_field="Football"
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.add_url = reverse("add_branch_gallery")
#         self.gallery_data = {
#             "gallery": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=",
#         }
#         self.client.post(self.add_url, self.gallery_data, format="json")
#         self.gallery = BranchGallery.objects.first()
#         self.url = reverse(
#             "delete_branch_gallery", kwargs={"gallery_id": self.gallery.id}
#         )

#     def test_gallery_delete_success(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(BranchGallery.objects.filter(id=self.gallery.id).exists())

#     def test_gallery_delete_without_authentication(self):
#         self.client.logout()
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_gallery_delete_unauthorized(self):
#         user = User.objects.create_user(
#             username="nonowner",
#             email="user@example.com",
#             password="password123",
#         )
#         self.client.force_authenticate(user=user)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


#     def test_gallery_delete_nonexistent_gallery(self):
#         self.gallery.delete()
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Gallery does not exist")


# class BranchMembersViewTests(APITestCase):
#     def setUp(self):
#         self.url = reverse("branch_members")
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )

#         self.user_trainee = User.objects.create_trainee(
#             email="trainee@example.com",
#             password="password123",
#         )
#         self.trainee = Trainee.objects.create(
#             user=self.user_trainee,
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.member = BranchMember.objects.create(
#             trainee=self.trainee,
#             branch=self.branch,
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             target_gender="male",
#             min_age=18,
#             max_age=40,
#             branch=self.branch,
#         )
#         self.subscription_plan = SubscriptionPlan.objects.get(
#             subscription=self.subscription,
#             duration=2,
#         )
#         self.member_subscription = MemberSubscription.objects.create(
#             subscription=self.subscription,
#             subscription_plan=self.subscription_plan,
#             member=self.member,
#             state="active",
#             start_date="2024-06-23",
#             end_date="2024-06-28",
#         )

#     def test_branch_members_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         response = self.client.get(self.url)
#         print("response.data branch member", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(
#             response.data[0]["trainee"]["user"]["email"], self.user_trainee.email
#         )

#     def test_branch_members_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_branch_members_without_authentication(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_branch_members_no_branch(self):
#         self.client.force_authenticate(user=self.user_owner)
#         self.branch.delete()  # Delete the branch to simulate a scenario where the owner has no branch
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Branch does not exist")


# class MemberSubscriptionUpdateViewTest(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )
#         self.user_trainee = User.objects.create_trainee(
#             email="trainee@example.com",
#             password="password123",
#         )
#         self.user_trainer = User.objects.create_trainer(
#             email="trainer@example.com",
#             password="password123",
#         )
#         self.trainer = Trainer.objects.create(
#             user=self.user_trainer,
#         )

#         self.trainee = Trainee.objects.create(
#             user=self.user_trainee,
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.branch_trainer = BranchTrainer.objects.create(
#             branch=self.branch,
#             trainer=self.trainer,
#         )
#         self.new_trainer = NewTrainer.objects.create(
#             username="newtrainer",
#             email="newtrainer@gmail.com",
#             branch=self.branch,
#         )
#         self.member = BranchMember.objects.create(
#             trainee=self.trainee,
#             branch=self.branch,
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             target_gender="male",
#             min_age=18,
#             max_age=40,
#             branch=self.branch,
#         )
#         self.subscription_plan = SubscriptionPlan.objects.get(
#             subscription=self.subscription,
#             duration=2,
#         )
#         self.subscription2 = Subscription.objects.create(
#             title="Boxing",
#             price=300.00,
#             target_gender="female",
#             branch=self.branch,
#         )
#         self.member_subscription = MemberSubscription.objects.create(
#             subscription=self.subscription,
#             subscription_plan=self.subscription_plan,
#             trainer=self.branch_trainer,
#             member=self.member,
#             state="active",
#             start_date="2024-06-23",
#             end_date="2024-06-28",
#         )

#     def test_member_subscription_update_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         data = {
#             "subscription_id": self.subscription2.id,
#             "new_trainer_id":self.new_trainer.id,
#         }
#         response = self.client.put(
#             reverse(
#                 "member_subscription_update",
#                 kwargs={"member_subscription_id": self.member_subscription.id},
#             ),
#             data,
#         )
#         print("member subs response.data", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["subscription"]["title"], self.subscription2.title)


#     def test_member_subscription_update_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         data = {
#             "subscription_id": self.subscription2.id,
#             "new_trainer_id":self.new_trainer.id,
#         }
#         response = self.client.put(
#             reverse(
#                 "member_subscription_update",
#                 kwargs={"member_subscription_id": self.member_subscription.id},
#             ),
#             data,
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_member_subscription_update_without_authentication(self):
#         data = {
#             "subscription_id": self.subscription2.id,
#             "new_trainer_id":self.new_trainer.id,
#         }
#         response = self.client.put(
#             reverse(
#                 "member_subscription_update",
#                 kwargs={"member_subscription_id": self.member_subscription.id},
#             ),
#             data,
#         )
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_member_subscription_update_nonexistent_subscription(self):
#         self.client.force_authenticate(user=self.user_owner)
#         self.member_subscription.delete()
#         data = {
#             "subscription_id": self.subscription2.id,
#             "new_trainer_id":self.new_trainer.id,
#         }
#         response = self.client.put(
#             reverse(
#                 "member_subscription_update",
#                 kwargs={"member_subscription_id": 3},
#             ),
#             data,
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Member subscription not found")


# class MemberSubscriptionDeleteViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )

#         self.user_trainee = User.objects.create_trainee(
#             email="trainee@example.com",
#             password="password123",
#         )
#         self.trainee = Trainee.objects.create(
#             user=self.user_trainee,
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.member = BranchMember.objects.create(
#             trainee=self.trainee,
#             branch=self.branch,
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             target_gender="male",
#             min_age=18,
#             max_age=40,
#             branch=self.branch,
#         )
#         self.subscription_plan = SubscriptionPlan.objects.get(
#             subscription=self.subscription,
#             duration=2,
#         )
#         self.member_subscription = MemberSubscription.objects.create(
#             subscription=self.subscription,
#             subscription_plan=self.subscription_plan,
#             member=self.member,
#             state="active",
#             start_date="2024-06-23",
#             end_date="2024-06-28",
#         )

#         self.url = reverse(
#             "member_subscription_delete",
#             kwargs={"member_subscription_id": self.member_subscription.id},
#         )

#     def test_member_subscription_delete_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         response = self.client.delete(self.url)
#         print("tttt response.data", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(
#             MemberSubscription.objects.filter(id=self.member_subscription.id).exists()
#         )

#     def test_member_subscription_delete_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_member_subscription_delete_without_authentication(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_member_subscription_delete_nonexistent_subscription(self):
#         self.client.force_authenticate(user=self.user_owner)
#         self.member_subscription.delete()
#         response = self.client.delete(self.url)
#         print("response.data nonexistent", response.data)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Member subscription not found")


# class BranchMemberDeleteViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )

#         self.user_trainee = User.objects.create_trainee(
#             email="trainee@example.com",
#             password="password123",
#         )
#         self.trainee = Trainee.objects.create(
#             user=self.user_trainee,
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.member = BranchMember.objects.create(
#             trainee=self.trainee,
#             branch=self.branch,
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             target_gender="male",
#             min_age=18,
#             max_age=40,
#             branch=self.branch,
#         )
#         self.subscription_plan = SubscriptionPlan.objects.get(
#             subscription=self.subscription,
#             duration=2,
#         )
#         self.member_subscription = MemberSubscription.objects.create(
#             subscription=self.subscription,
#             subscription_plan=self.subscription_plan,
#             member=self.member,
#             state="active",
#             start_date="2024-06-23",
#             end_date="2024-06-28",
#         )

#         self.url = reverse(
#             "branch_member_delete",
#             kwargs={"member_id": self.member.id},
#         )

#     def test_branch_member_delete_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         response = self.client.delete(self.url)
#         print("tttt response.data", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(BranchMember.objects.filter(id=self.member.id).exists())

#     def test_branch_member_delete_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_branch_member_delete_without_authentication(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_branch_member_delete_nonexistent_member(self):
#         self.client.force_authenticate(user=self.user_owner)
#         self.member.delete()
#         response = self.client.delete(self.url)
#         print("response.data nonexistent", response.data)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Branch member not found")


# class NewTrainerConvertViewTests(APITestCase):
#     def setUp(self):
#         # Create a user with owner permissions
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         # Create a non-owner user
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )
#         # Create a club
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         # Create a branch under the club
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         print("branch is here", self.branch.id)
#         # Create a trainer user
#         self.trainer_user = User.objects.create_trainer(
#             email="trainer@example.com",
#             password="password123",
#         )
#         # Create a trainer profile
#         self.trainer = Trainer.objects.create(
#             user=self.trainer_user,
#         )
#         # Add New Trainer to the branch
#         self.new_trainer = NewTrainer.objects.create(
#             email="newTrainer@example.com",
#             username="newTrainer",
#             branch=self.branch,
#         )
#         # URL for the NewTrainerConvertView
#         self.url = reverse(
#             "new_trainer_convert", kwargs={"new_trainer_id": self.new_trainer.id}
#         )

#     def test_new_trainer_convert_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         data = {"trainer_slug": self.trainer.slug}
#         response = self.client.post(self.url, data, format="json")
#         print("new trainer convert response", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(Trainer.objects.filter(user=self.trainer_user).exists())
#         self.assertFalse(NewTrainer.objects.filter(id=self.new_trainer.id).exists())

#     def test_new_trainer_convert_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         data = {"trainer_slug": self.trainer.slug}
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_new_trainer_convert_without_authentication(self):
#         data = {"trainer_slug": self.trainer.slug}
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_new_trainer_convert_invalid_trainer(self):
#         self.client.force_authenticate(user=self.user_owner)
#         data = {"trainer_slug": "invalid_slug"}
#         response = self.client.post(self.url, data, format="json")
#         print("response.data invalid trainer", response.data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Trainer not found")

#     def test_new_trainer_convert_invalid_new_trainer(self):
#         self.client.force_authenticate(user=self.user_owner)
#         data = {"trainer_slug": self.trainer.slug}
#         invalid_url = reverse("new_trainer_convert", kwargs={"new_trainer_id": 100})
#         response = self.client.post(invalid_url, data, format="json")
#         print("response.data invalid new trainer", response.data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "New Trainer not found")


# class NewTrainerDeleteViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owneruser@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.new_trainer = NewTrainer.objects.create(
#             email="newtrainer@example.com",
#             username="newtrainer",
#             branch=self.branch,
#         )

#         self.url = reverse(
#             "new_trainer_delete", kwargs={"new_trainer_id": self.new_trainer.id}
#         )

#     def test_new_trainer_delete_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(NewTrainer.objects.filter(id=self.new_trainer.id).exists())

#     def test_new_trainer_delete_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_new_trainer_delete_without_authentication(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_new_trainer_delete_invalid_new_trainer(self):
#         self.client.force_authenticate(user=self.user_owner)
#         invalid_url = reverse("new_trainer_delete", kwargs={"new_trainer_id": 100})
#         response = self.client.delete(invalid_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "New Trainer not found")


# class NewTrainerUpdateViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owneruser@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.new_trainer = NewTrainer.objects.create(
#             email="newtrainer@example.com",
#             username="newtrainer",
#             branch=self.branch,
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             branch=self.branch,
#         )
#         # URL for the NewTrainerUpdateView
#         self.url = reverse(
#             "new_trainer_update",
#             kwargs={"new_trainer_id": self.new_trainer.id},
#         )

#     def test_new_trainer_update_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         subscription_id=self.subscription.id
#         print('here subscription_id', subscription_id)
#         data = {
#             "username": "Hussein",
#             "phone_number": "1234567890",
#             "profile_picture": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=",
#             "subscriptions":[
#                 subscription_id
#             ]
#         }
#         print('profile_pic',data)
#         response = self.client.patch(self.url, data, format="json")
#         print("response.data new trainer update", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.new_trainer.refresh_from_db()
#         self.assertEqual(self.new_trainer.username, data["username"])
#         self.assertEqual(self.new_trainer.phone_number, data["phone_number"])


#     def test_new_trainer_update_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         data = {
#             "username": "Hussein",
#             "phone_number":"1234567890"
#         }
#         response = self.client.patch(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_new_trainer_update_without_authentication(self):
#         data = {
#             "username": "Hussein",
#             "phone_number":"1234567890"
#         }
#         response = self.client.patch(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_new_trainer_update_invalid_new_trainer(self):
#         self.client.force_authenticate(user=self.user_owner)
#         invalid_url = reverse("new_trainer_update", kwargs={"new_trainer_id": 100})
#         data = {
#             "username": "Hussein",
#             "phone_number":"1234567890"
#         }
#         response = self.client.patch(invalid_url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "New Trainer not found")

#     def test_new_trainer_update_invalid_data(self):
#         self.client.force_authenticate(user=self.user_owner)
#         data = {
#             "username": "Hussein",
#             "phone_number":"1234567890",
#             "profile_picture": "invalid_image"
#         }
#         response = self.client.patch(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)


# class BranchReviewsViewTests(APITestCase):
#     def setUp(self):
#         # Create a user
#         self.owner = User.objects.create_owner(
#             username="owner",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.trainee = User.objects.create_trainee(
#             email="trainee@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(property_name="Test Club")
#         self.branch = Branch.objects.create(
#             owner=self.owner,
#             club=self.club,
#             address="123 Test St",
#         )
#         self.trainee = Trainee.objects.create(user=self.trainee)

#         # Create a review
#         review_content_type = ContentType.objects.get_for_model(Branch)
#         self.review = Review.objects.create(
#             ratings=5,
#             comment="Great experience!",
#             trainee=self.trainee,
#             content_type=review_content_type,
#             object_id=self.branch.id,
#         )
#         self.url = reverse("branch_reviews")

#         # Authenticate the user
#         self.client.force_authenticate(user=self.owner)

#     def test_branch_reviews_success(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]["ratings"], self.review.ratings)
#         self.assertEqual(response.data[0]["comment"], self.review.comment)

#     def test_branch_reviews_without_authentication(self):
#         self.client.logout()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_branch_reviews_no_reviews(self):
#         self.review.delete()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 0)

#     def test_branch_reviews_invalid_branch(self):
#         self.review.delete()
#         self.branch.delete()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Branch does not exist")


# class NewTrainerAddViewTests(APITestCase):
#     def setUp(self):
#         self.url = reverse("new_trainer_add")
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.trainer_data = {
#             "email": "trainer@example.com",
#             "username": "traineruser",
#             "profile_picture": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII=",
#             "phone_number": "1234567890",
#             "subscriptions": [],
#         }

#     def test_new_trainer_add_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         response = self.client.post(self.url, self.trainer_data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["email"], self.trainer_data["email"])
#         self.assertEqual(response.data["username"], self.trainer_data["username"])
#         self.assertTrue(
#             NewTrainer.objects.filter(email=self.trainer_data["email"]).exists()
#         )

#     def test_new_trainer_add_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.post(self.url, self.trainer_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_new_trainer_add_without_authentication(self):
#         response = self.client.post(self.url, self.trainer_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_new_trainer_add_missing_required_fields(self):
#         self.client.force_authenticate(user=self.user_owner)
#         incomplete_data = self.trainer_data.copy()
#         del incomplete_data["email"]  # Remove a required field
#         response = self.client.post(self.url, incomplete_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)


# class BranchSubscriptionsViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.client.force_authenticate(user=self.user_owner)
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="user@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             target_gender="male",
#             min_age=18,
#             max_age=40,
#             branch=self.branch,
#         )
#         self.url = reverse("branch_subscriptions")

#     def test_branch_subscriptions_success(self):
#         response = self.client.get(self.url)
#         print("subscriptions response.data", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]["title"], self.subscription.title)

#     def test_branch_subscriptions_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.get(self.url)
#         print('unauth response',response.data)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "You are not authorized to perform this action")

#     def test_branch_subscriptions_without_authentication(self):
#         self.client.logout()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_branch_subscriptions_no_subscriptions(self):
#         self.subscription.delete()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 0)
#         self.assertEqual(response.data, [])


# class BranchSubscriptionPlanDeleteViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )

#         self.user_trainee = User.objects.create_trainee(
#             email="trainee@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             target_gender="male",
#             min_age=18,
#             max_age=40,
#             branch=self.branch,
#         )
#         self.subscription_plan = SubscriptionPlan.objects.get(
#             subscription=self.subscription,
#             duration=2,
#         )
#         self.url = reverse(
#             "branch_subscription_plan_delete",
#             kwargs={"subscription_plan_id": self.subscription_plan.id},
#         )

#         self.client.force_authenticate(user=self.user_owner)

#     def test_subscription_plan_delete_success(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(
#             SubscriptionPlan.objects.filter(id=self.subscription_plan.id).exists()
#         )

#     def test_subscription_plan_delete_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_subscription_plan_delete_without_authentication(self):
#         self.client.logout()
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_subscription_plan_delete_invalid_subscription_plan(self):
#         self.subscription_plan.delete()
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Subscription Plan not found")


# class BranchSubscriptionAddViewTests(APITestCase):
#     def setUp(self):
#         self.url = reverse("branch_subscription_add")
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.client.force_authenticate(user=self.user_owner)
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.subscription_data = {
#             "title": "Fitness",
#             "target_gender": "male",
#             "price": 100.00,
#             "min_age": 18,
#             "max_age": 40,
#             "subscription_plan": [
#                 {
#                     "duration": 2,
#                     "price": 500,
#                 }
#             ],
#         }

#     def test_subscription_add_success(self):
#         response = self.client.post(self.url, self.subscription_data, format="json")
#         print("response.data right noewww", response.data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         subscription = Subscription.objects.get(branch=self.branch)
#         subscription_plan = SubscriptionPlan.objects.get(
#             subscription=subscription, duration=2
#         )
#         self.assertTrue(Subscription.objects.filter(branch=self.branch).exists())
#         self.assertEqual(subscription_plan.price, 500)
#         self.assertEqual(subscription_plan.duration, 2)
#         self.assertEqual(subscription.title, "Fitness")
#         all_subscription_plans = SubscriptionPlan.objects.filter(
#             subscription=subscription
#         )
#         print("all_subscription_plans", all_subscription_plans.values())
#         self.assertEqual(all_subscription_plans.count(), 12)

#     def test_subscription_add_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.post(self.url, self.subscription_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_subscription_add_without_authentication(self):
#         self.client.logout()
#         response = self.client.post(self.url, self.subscription_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_subscription_add_invalid_data(self):
#         invalid_data = self.subscription_data.copy()
#         invalid_data["title"] = ""
#         response = self.client.post(self.url, invalid_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)


# class BranchSubscriptionUpdateViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.client.force_authenticate(user=self.user_owner)
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="user@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             target_gender="male",
#             min_age=18,
#             max_age=40,
#             branch=self.branch,
#         )
#         self.update_data = {
#             "title": "Yoga",
#             "price": Decimal("200.00"),
#             "min_age": 20,
#             "max_age": 50,
#             "active": True,
#             "subscription_plans": [
#                 {
#                     "duration": 1,
#                     "price": 600,
#                 }
#             ],
#         }
#         self.url = reverse(
#             "branch_subscription_update",
#             kwargs={"subscription_id": self.subscription.id},
#         )

#     def test_subscription_update_success(self):
#         response = self.client.put(self.url, self.update_data, format="json")
#         print("response.data diff", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         subscription = Subscription.objects.get(branch=self.branch)
#         subscription_plan = SubscriptionPlan.objects.get(
#             subscription=subscription, duration=1
#         )
#         self.assertEqual(subscription.title, "Yoga")
#         self.assertEqual(subscription.price, 200.00)
#         self.assertEqual(subscription.min_age, 20)
#         self.assertEqual(subscription.max_age, 50)
#         self.assertEqual(subscription_plan.price, 600)
#         self.assertEqual(subscription_plan.duration, 1)
#         all_subscription_plans = SubscriptionPlan.objects.filter(
#             subscription=subscription
#         )
#         self.assertEqual(all_subscription_plans.count(), 12)

#     def test_subscription_update_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.put(self.url, self.update_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_subscription_update_without_authentication(self):
#         self.client.logout()
#         response = self.client.put(self.url, self.update_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_subscription_update_invalid_data(self):
#         invalid_data = self.update_data.copy()
#         invalid_data["title"] = ""
#         response = self.client.put(self.url, invalid_data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("error", response.data)


# class BranchSubscriptionDeleteViewTests(APITestCase):
#     def setUp(self):
#         self.user_owner = User.objects.create_owner(
#             username="owneruser",
#             email="owner@example.com",
#             password="password123",
#         )
#         self.user_non_owner = User.objects.create_user(
#             username="nonowneruser",
#             email="nonowner@example.com",
#             password="password123",
#         )
#         self.another_owner = User.objects.create_owner(
#             username="nonowneruser",
#             email="anohterowner@example.com",
#             password="password123",
#         )
#         self.club = Club.objects.create(
#             property_name="Test Club",
#             sport_field="Football",
#         )
#         self.branch = Branch.objects.create(
#             owner=self.user_owner,
#             club=self.club,
#             address="123 Test St",
#             details="Test details",
#         )
#         self.subscription = Subscription.objects.create(
#             title="Fitness",
#             price=100.00,
#             branch=self.branch,
#         )
#         print("id here", self.subscription.id)
#         self.url = reverse(
#             "branch_subscription_delete",
#             kwargs={"subscription_id": self.subscription.id},
#         )

#     def test_subscription_delete_success(self):
#         self.client.force_authenticate(user=self.user_owner)
#         response = self.client.delete(self.url)
#         print("response.data temmmpp", response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["message"], "Subscription deleted successfully")
#         self.assertFalse(Subscription.objects.filter(id=self.subscription.id).exists())

#     def test_subscription_delete_unauthorized(self):
#         self.client.force_authenticate(user=self.user_non_owner)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertIn("error", response.data)
#         self.assertEqual(
#             response.data["error"], "You are not authorized to perform this action"
#         )

#     def test_subscription_delete_without_authentication(self):
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_subscription_delete_nonexistent_subscription(self):
#         self.client.force_authenticate(user=self.user_owner)
#         # Change the subscription ID to a nonexistent one
#         nonexistent_url = reverse(
#             "branch_subscription_delete", kwargs={"subscription_id": 999}
#         )
#         response = self.client.delete(nonexistent_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Subscription not found")

#     def test_subscription_delete_wrong_branch(self):
#         # Create another branch and try to delete the subscription from it

#         another_branch = Branch.objects.create(
#             owner=self.another_owner,
#             club=self.club,
#             address="456 Another St",
#             details="Another details",
#         )
#         self.client.force_authenticate(user=self.another_owner)
#         response = self.client.delete(self.url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "Subscription not found")
