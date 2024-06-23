# from django.test import TestCase
# from clubs.models import (
#     Attendance,
#     Branch,
#     BranchMember,
#     BranchTrainer,
#     Club,
#     ContactUs,
#     Document,
#     Facilities,
#     MemberSubscription,
#     NewTrainer,
#     Subscription,
#     SubscriptionPlan,
#     Time,
#     WorkingHours,
# )

# from django.contrib.auth import get_user_model

# from trainings.models import Trainee, Trainer

# from datetime import timedelta
# from django.utils import timezone
# from datetime import datetime

# User = get_user_model()


# class ClubModelTest(TestCase):
#     @classmethod
#     def setUpTestData(self):
#         # Set up non-modified objects used by all test methods
#         self.club = Club.objects.create(
#             property_name="Test Club", country="Test Country"
#         )

#     def test_property_name_label(self):
#         field_label = self.club._meta.get_field("property_name").verbose_name
#         self.assertEqual(field_label, "property name")

#     def test_country_label(self):
#         field_label = self.club._meta.get_field("country").verbose_name
#         self.assertEqual(field_label, "country")

#     def test_property_name_max_length(self):
#         max_length = self.club._meta.get_field("property_name").max_length
#         self.assertEqual(max_length, 255)

#     def test_country_max_length(self):
#         max_length = self.club._meta.get_field("country").max_length
#         self.assertEqual(max_length, 255)

#     def test_object_name_is_property_name(self):
#         expected_object_name = f"{self.club.property_name} Club"
#         self.assertEqual(expected_object_name, str(self.club))


# class BranchModelTest(TestCase):
#     @classmethod
#     def setUpTestData(self):
#         # Set up non-modified objects used by all test methods
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         User.objects.create_owner(
#             username="testuser",
#             email="testuser@test.com",
#             password="12345",
#         )
#         user = User.objects.get(username="testuser")
#         self.branch = Branch.objects.create(
#             owner=user, club=club, address="Test Address"
#         )

#     def test_owner_label(self):
#         field_label = self.branch._meta.get_field("owner").verbose_name
#         self.assertEqual(field_label, "owner")

#     def test_address_label(self):
#         field_label = self.branch._meta.get_field("address").verbose_name
#         self.assertEqual(field_label, "address")

#     def test_address_max_length(self):
#         max_length = self.branch._meta.get_field("address").max_length
#         self.assertEqual(max_length, 255)

#     def test_default_values(self):
#         self.assertEqual(self.branch.current_balance, 0.0)
#         self.assertEqual(self.branch.total_balance, 0.0)
#         self.assertEqual(self.branch.total_members, 0)
#         self.assertEqual(self.branch.new_members, 0)
#         self.assertEqual(self.branch.is_verified, False)
#         self.assertEqual(self.branch.is_open, False)
#         self.assertEqual(self.branch.avg_ratings, 0.0)
#         self.assertEqual(self.branch.number_of_ratings, 0)

#     def test_object_name_is_property_name(self):
#         expected_object_name = self.branch.club.property_name
#         self.assertEqual(expected_object_name, str(self.branch))


# class DocumentModelTest(TestCase):
#     @classmethod
#     def setUpTestData(self):
#         # Set up non-modified objects used by all test methods
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         self.document = Document.objects.create(club=club, document="Test Document")

#     def test_document_label(self):
#         field_label = self.document._meta.get_field("document").verbose_name
#         self.assertEqual(field_label, "document")

#     def test_club_label(self):
#         field_label = self.document._meta.get_field("club").verbose_name
#         self.assertEqual(field_label, "club")

#     def test_created_at_label(self):
#         field_label = self.document._meta.get_field("created_at").verbose_name
#         self.assertEqual(field_label, "created at")

#     def test_object_name_is_property_name(self):
#         expected_object_name = self.document.club.property_name
#         self.assertEqual(expected_object_name, str(self.document))


# class SubscriptionModelTest(TestCase):
#     @classmethod
#     def setUpTestData(self):
#         # Set up non-modified objects used by all test methods
#         owner = User.objects.create_owner(
#             username="testuser",
#             email="testuser@test.com",
#             password="12345",
#         )
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         branch = Branch.objects.create(club=club, address="Test Address", owner=owner)
#         self.subscription = Subscription.objects.create(
#             title="Test Subscription", branch=branch
#         )

#     def test_title_label(self):
#         field_label = self.subscription._meta.get_field("title").verbose_name
#         self.assertEqual(field_label, "title")

#     def test_target_gender_label(self):
#         field_label = self.subscription._meta.get_field("target_gender").verbose_name
#         self.assertEqual(field_label, "target gender")

#     def test_price_label(self):
#         field_label = self.subscription._meta.get_field("price").verbose_name
#         self.assertEqual(field_label, "price")

#     def test_active_label(self):
#         field_label = self.subscription._meta.get_field("active").verbose_name
#         self.assertEqual(field_label, "active")

#     def test_min_age_label(self):
#         field_label = self.subscription._meta.get_field("min_age").verbose_name
#         self.assertEqual(field_label, "min age")

#     def test_max_age_label(self):
#         field_label = self.subscription._meta.get_field("max_age").verbose_name
#         self.assertEqual(field_label, "max age")

#     def test_branch_label(self):
#         field_label = self.subscription._meta.get_field("branch").verbose_name
#         self.assertEqual(field_label, "branch")

#     def test_is_completed_label(self):
#         field_label = self.subscription._meta.get_field("is_completed").verbose_name
#         self.assertEqual(field_label, "is completed")

#     def test_max_members_label(self):
#         field_label = self.subscription._meta.get_field("max_members").verbose_name
#         self.assertEqual(field_label, "max members")

#     def test_current_members_count_label(self):
#         field_label = self.subscription._meta.get_field(
#             "current_members_count"
#         ).verbose_name
#         self.assertEqual(field_label, "current members count")

#     def test_default_values(self):
#         self.assertEqual(self.subscription.target_gender, "both")
#         self.assertEqual(self.subscription.price, 0.0)
#         self.assertEqual(self.subscription.active, True)
#         self.assertEqual(self.subscription.min_age, 18)
#         self.assertEqual(self.subscription.max_age, 99)
#         self.assertEqual(self.subscription.is_completed, False)
#         self.assertEqual(self.subscription.max_members, None)
#         self.assertEqual(self.subscription.current_members_count, 0)

#     def test_object_name_is_title(self):
#         expected_object_name = self.subscription.title
#         self.assertEqual(expected_object_name, str(self.subscription))


# class SubscriptionPlanModelTest(TestCase):
#     @classmethod
#     def setUpTestData(self):
#         # Set up non-modified objects used by all test methods
#         self.subscriptionPlan = SubscriptionPlan.objects.create(duration=6, price=100.0)

#     def test_is_added_label(self):
#         field_label = self.subscriptionPlan._meta.get_field("is_added").verbose_name
#         self.assertEqual(field_label, "is added")

#     def test_duration_label(self):
#         field_label = self.subscriptionPlan._meta.get_field("duration").verbose_name
#         self.assertEqual(field_label, "duration")

#     def test_price_label(self):
#         field_label = self.subscriptionPlan._meta.get_field("price").verbose_name
#         self.assertEqual(field_label, "price")

#     def test_is_offer_label(self):
#         field_label = self.subscriptionPlan._meta.get_field("is_offer").verbose_name
#         self.assertEqual(field_label, "is offer")

#     def test_current_members_count_label(self):
#         field_label = self.subscriptionPlan._meta.get_field(
#             "current_members_count"
#         ).verbose_name
#         self.assertEqual(field_label, "current members count")

#     def test_max_members_label(self):
#         field_label = self.subscriptionPlan._meta.get_field("max_members").verbose_name
#         self.assertEqual(field_label, "max members")

#     def test_expiration_date_label(self):
#         field_label = self.subscriptionPlan._meta.get_field(
#             "expiration_date"
#         ).verbose_name
#         self.assertEqual(field_label, "expiration date")

#     def test_subscription_label(self):
#         field_label = self.subscriptionPlan._meta.get_field("subscription").verbose_name
#         self.assertEqual(field_label, "subscription")

#     def test_created_at_label(self):
#         field_label = self.subscriptionPlan._meta.get_field("created_at").verbose_name
#         self.assertEqual(field_label, "created at")

#     def test_updated_at_label(self):
#         field_label = self.subscriptionPlan._meta.get_field("updated_at").verbose_name
#         self.assertEqual(field_label, "updated at")

#     def test_default_values(self):
#         self.assertEqual(self.subscriptionPlan.is_added, False)
#         self.assertEqual(self.subscriptionPlan.price, 100.0)
#         self.assertEqual(self.subscriptionPlan.is_offer, False)
#         self.assertEqual(self.subscriptionPlan.current_members_count, 0)
#         self.assertEqual(self.subscriptionPlan.max_members, None)

#     def test_object_name_is_duration(self):
#         expected_object_name = f"{self.subscriptionPlan.duration} months"
#         self.assertEqual(expected_object_name, str(self.subscriptionPlan))


# class NewTrainerModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.new_trainer = NewTrainer.objects.create(
#             email="test@test.com", username="testuser", phone_number="1234567890"
#         )

#     def test_email_label(self):
#         field_label = self.new_trainer._meta.get_field("email").verbose_name
#         self.assertEqual(field_label, "email")

#     def test_branch_label(self):
#         field_label = self.new_trainer._meta.get_field("branch").verbose_name
#         self.assertEqual(field_label, "branch")

#     def test_profile_picture_label(self):
#         field_label = self.new_trainer._meta.get_field("profile_picture").verbose_name
#         self.assertEqual(field_label, "profile picture")

#     def test_members_count_label(self):
#         field_label = self.new_trainer._meta.get_field("members_count").verbose_name
#         self.assertEqual(field_label, "members count")

#     def test_username_label(self):
#         field_label = self.new_trainer._meta.get_field("username").verbose_name
#         self.assertEqual(field_label, "username")

#     def test_phone_number_label(self):
#         field_label = self.new_trainer._meta.get_field("phone_number").verbose_name
#         self.assertEqual(field_label, "phone number")

#     def test_subscriptions_label(self):
#         field_label = self.new_trainer._meta.get_field("subscriptions").verbose_name
#         self.assertEqual(field_label, "subscriptions")

#     def test_created_at_label(self):
#         field_label = self.new_trainer._meta.get_field("created_at").verbose_name
#         self.assertEqual(field_label, "created at")

#     def test_updated_at_label(self):
#         field_label = self.new_trainer._meta.get_field("updated_at").verbose_name
#         self.assertEqual(field_label, "updated at")

#     def test_default_values(self):
#         self.assertEqual(self.new_trainer.members_count, 0)
#         self.assertEqual(self.new_trainer.profile_picture, "profile_pics/default.png")

#     def test_object_name_is_username(self):
#         expected_object_name = self.new_trainer.username
#         self.assertEqual(expected_object_name, str(self.new_trainer))


# class BranchTrainerModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         user = User.objects.create_trainer(
#             email="testuser@test.com",
#             password="12345",
#         )
#         trainer = Trainer.objects.create(user=user)
#         owner = User.objects.create_owner(
#             username="testuser",
#             email="owener@test.com",
#             password="12345",
#         )
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         branch = Branch.objects.create(club=club, address="Test Address", owner=owner)
#         cls.branch_trainer = BranchTrainer.objects.create(
#             trainer=trainer, branch=branch
#         )

#     def test_trainer_label(self):
#         field_label = self.branch_trainer._meta.get_field("trainer").verbose_name
#         self.assertEqual(field_label, "trainer")

#     def test_branch_label(self):
#         field_label = self.branch_trainer._meta.get_field("branch").verbose_name
#         self.assertEqual(field_label, "branch")

#     def test_subscriptions_label(self):
#         field_label = self.branch_trainer._meta.get_field("subscriptions").verbose_name
#         self.assertEqual(field_label, "subscriptions")

#     def test_members_count_label(self):
#         field_label = self.branch_trainer._meta.get_field("members_count").verbose_name
#         self.assertEqual(field_label, "members count")

#     def test_created_at_label(self):
#         field_label = self.branch_trainer._meta.get_field("created_at").verbose_name
#         self.assertEqual(field_label, "created at")

#     def test_updated_at_label(self):
#         field_label = self.branch_trainer._meta.get_field("updated_at").verbose_name
#         self.assertEqual(field_label, "updated at")

#     def test_default_values(self):
#         self.assertEqual(self.branch_trainer.members_count, 0)

#     def test_object_name_is_trainer(self):
#         expected_object_name = f"{self.branch_trainer.trainer}"
#         self.assertEqual(expected_object_name, str(self.branch_trainer))


# class BranchMemberModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         user = User.objects.create_trainee(
#             email="testuser@test.com",
#             password="12345",
#         )
#         trainee = Trainee.objects.create(user=user)
#         owner = User.objects.create_owner(
#             username="testuser",
#             email="owener@test.com",
#             password="12345",
#         )
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         branch = Branch.objects.create(club=club, address="Test Address", owner=owner)
#         cls.branch_member = BranchMember.objects.create(trainee=trainee, branch=branch)

#     def test_trainee_label(self):
#         field_label = self.branch_member._meta.get_field("trainee").verbose_name
#         self.assertEqual(field_label, "trainee")

#     def test_branch_label(self):
#         field_label = self.branch_member._meta.get_field("branch").verbose_name
#         self.assertEqual(field_label, "branch")

#     def test_created_at_label(self):
#         field_label = self.branch_member._meta.get_field("created_at").verbose_name
#         self.assertEqual(field_label, "created at")

#     def test_updated_at_label(self):
#         field_label = self.branch_member._meta.get_field("updated_at").verbose_name
#         self.assertEqual(field_label, "updated at")

#     def test_object_name_is_trainee(self):
#         expected_object_name = f"{self.branch_member.trainee}"
#         self.assertEqual(expected_object_name, str(self.branch_member))


# class MemberSubscriptionModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         user = User.objects.create_trainee(
#             email="testuser@test.com",
#             password="12345",
#         )
#         trainee = Trainee.objects.create(user=user)
#         owner = User.objects.create_owner(
#             username="testuser",
#             email="owener@test.com",
#             password="12345",
#         )
#         trainer_user = User.objects.create_trainer(
#             email="trainer@test.com",
#             password="12345",
#         )
#         trainer = Trainer.objects.create(user=trainer_user)
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         branch = Branch.objects.create(club=club, address="Test Address", owner=owner)
#         branch_member = BranchMember.objects.create(trainee=trainee, branch=branch)
#         branch_trainer = BranchTrainer.objects.create(trainer=trainer, branch=branch)
#         subscription = Subscription.objects.create(
#             title="Test Subscription", branch=branch
#         )
#         subscription_plan = SubscriptionPlan.objects.get(
#             subscription=subscription,
#             duration=6,
#         )
#         cls.member_subscription = MemberSubscription.objects.create(
#             member=branch_member,
#             trainer=branch_trainer,
#             subscription_plan=subscription_plan,
#             subscription=subscription,
#             state="active",
#         )

#     def test_member_label(self):
#         field_label = self.member_subscription._meta.get_field("member").verbose_name
#         self.assertEqual(field_label, "member")

#     def test_trainer_label(self):
#         field_label = self.member_subscription._meta.get_field("trainer").verbose_name
#         self.assertEqual(field_label, "trainer")

#     def test_subscription_plan_label(self):
#         field_label = self.member_subscription._meta.get_field(
#             "subscription_plan"
#         ).verbose_name
#         self.assertEqual(field_label, "subscription plan")

#     def test_subscription_label(self):
#         field_label = self.member_subscription._meta.get_field(
#             "subscription"
#         ).verbose_name
#         self.assertEqual(field_label, "subscription")

#     def test_state_label(self):
#         field_label = self.member_subscription._meta.get_field("state").verbose_name
#         self.assertEqual(field_label, "state")

#     def test_start_date_label(self):
#         field_label = self.member_subscription._meta.get_field(
#             "start_date"
#         ).verbose_name
#         self.assertEqual(field_label, "start date")

#     def test_end_date_label(self):
#         field_label = self.member_subscription._meta.get_field("end_date").verbose_name
#         self.assertEqual(field_label, "end date")

#     def test_object_name_is_member_subscription_plan(self):
#         expected_object_name = f"{self.member_subscription.member} - {self.member_subscription.subscription_plan}"
#         self.assertEqual(expected_object_name, str(self.member_subscription))


# class AttendanceModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         user = User.objects.create_trainee(
#             email="testuser@test.com",
#             password="12345",
#         )
#         trainee = Trainee.objects.create(user=user)
#         owner = User.objects.create_owner(
#             username="testuser",
#             email="owener@test.com",
#             password="12345",
#         )
#         trainer_user = User.objects.create_trainer(
#             email="trainer@test.com",
#             password="12345",
#         )
#         trainer = Trainer.objects.create(user=trainer_user)
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         branch = Branch.objects.create(club=club, address="Test Address", owner=owner)
#         branch_member = BranchMember.objects.create(trainee=trainee, branch=branch)
#         branch_trainer = BranchTrainer.objects.create(trainer=trainer, branch=branch)
#         subscription = Subscription.objects.create(
#             title="Test Subscription", branch=branch
#         )
#         subscription_plan = SubscriptionPlan.objects.get(
#             subscription=subscription,
#             duration=6,
#         )
#         member_subscription = MemberSubscription.objects.create(
#             member=branch_member,
#             trainer=branch_trainer,
#             subscription_plan=subscription_plan,
#             subscription=subscription,
#             state="active",
#         )
#         cls.attendance = Attendance.objects.create(
#             day="2021-08-01",
#             member_subscription=member_subscription,
#         )

#     def test_day_label(self):
#         field_label = self.attendance._meta.get_field("day").verbose_name
#         self.assertEqual(field_label, "day")

#     def test_branch_member_label(self):
#         field_label = self.attendance._meta.get_field(
#             "member_subscription"
#         ).verbose_name
#         self.assertEqual(field_label, "member subscription")

#     def test_date_label(self):
#         field_label = self.attendance._meta.get_field("date").verbose_name
#         self.assertEqual(field_label, "date")

#     def test_is_present_label(self):
#         field_label = self.attendance._meta.get_field("is_present").verbose_name
#         self.assertEqual(field_label, "is present")

#     def test_is_present_default(self):
#         self.assertEqual(self.attendance.is_present, False)

#     def test_object_name(self):
#         expected_object_name = f"{self.attendance.member_subscription}"
#         self.assertEqual(str(self.attendance), expected_object_name + " - 2021-08-01")


# class ContactUsModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         User.objects.create_owner(
#             username="testuser",
#             email="testuser@test.com",
#             password="12345",
#         )
#         user = User.objects.get(username="testuser")
#         branch = Branch.objects.create(
#             owner=user, club=club, address="Test Address"
#         )
#         cls.contactus = ContactUs.objects.create(
#             message="Test Message", branch=branch
#         )

#     def test_message_label(self):
#         field_label = self.contactus._meta.get_field("message").verbose_name
#         self.assertEqual(field_label, "message")

#     def test_branch_label(self):
#         field_label = self.contactus._meta.get_field("branch").verbose_name
#         self.assertEqual(field_label, "branch")

#     def test_created_at_label(self):
#         field_label = self.contactus._meta.get_field("created_at").verbose_name
#         self.assertEqual(field_label, "created at")

#     def test_message_max_length(self):
#         max_length = self.contactus._meta.get_field("message").max_length
#         self.assertEqual(max_length, None)

#     def test_object_name_is_message(self):
#         expected_object_name = f"{self.contactus.message}"
#         self.assertEqual(expected_object_name, str(self.contactus))


# class WorkingHoursModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         User.objects.create_owner(
#             username="testuser",
#             email="testuser@test.com",
#             password="12345",
#         )
#         user = User.objects.get(username="testuser")
#         branch = Branch.objects.create(
#             owner=user, club=club, address="Test Address"
#         )
#         cls.working_hours = WorkingHours.objects.create(
#             day="Monday", is_open=True, branch=branch
#         )

#     def test_str_method(self):
#         expected_object_name = (
#             f"{self.working_hours.get_day_display()} - Active: {self.working_hours.is_open}"
#         )
#         self.assertEqual(expected_object_name, str(self.working_hours))

#     def test_day_label(self):
#         field_label = self.working_hours._meta.get_field("day").verbose_name
#         self.assertEqual(field_label, "day")

#     def test_is_open_label(self):
#         field_label = self.working_hours._meta.get_field("is_open").verbose_name
#         self.assertEqual(field_label, "is open")

#     def test_branch_label(self):
#         field_label = self.working_hours._meta.get_field("branch").verbose_name
#         self.assertEqual(field_label, "branch")

#     def test_day_max_length(self):
#         max_length = self.working_hours._meta.get_field("day").max_length
#         self.assertEqual(max_length, 255)

#     def test_day_choices(self):
#         choices = self.working_hours._meta.get_field("day").choices
#         self.assertEqual(
#             choices,
#             [
#                 ("Monday", "Monday"),
#                 ("Tuesday", "Tuesday"),
#                 ("Wednesday", "Wednesday"),
#                 ("Thursday", "Thursday"),
#                 ("Friday", "Friday"),
#                 ("Saturday", "Saturday"),
#                 ("Sunday", "Sunday"),
#             ],
#         )

#     def test_is_open_default(self):
#         default = self.working_hours._meta.get_field("is_open").default
#         self.assertEqual(default, False)


# class TimeModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Setup required models for Time model testing
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         User.objects.create_owner(
#             username="testuser",
#             email="testuser@test.com",
#             password="12345",
#         )
#         user = User.objects.get(username="testuser")
#         branch = Branch.objects.create(
#             owner=user, club=club, address="Test Address"
#         )
#         cls.working_hours = WorkingHours.objects.create(
#             day="Monday", is_open=True, branch=branch
#         )
#         cls.time = Time.objects.create(from_time="09:00", to_time="17:00", day=cls.working_hours)

#     def test_time_before_opening(self):
#         # Set current time before opening time
#         self.time.from_time = "10:00"
#         self.time.to_time = "17:00"
#         self.time.save()
#         self.assertFalse(self.working_hours.is_open)

#     def test_time_during_opening_hours(self):
#         # Convert current time to a full datetime object
#         now_datetime = timezone.now()

#         # Perform arithmetic operations with timedelta
#         from_time_datetime = now_datetime - timedelta(hours=1)
#         to_time_datetime = now_datetime + timedelta(hours=1)

#         # Extract the time part and format it
#         self.time.from_time = from_time_datetime.time().strftime("%H:%M")
#         self.time.to_time = to_time_datetime.time().strftime("%H:%M")
#         self.time.save()

#         self.assertTrue(self.working_hours.is_open)

#     def test_time_after_closing(self):
#         # Set current time after closing time
#         self.time.from_time = "09:00"
#         self.time.to_time = "17:00"
#         self.time.save()
#         self.assertFalse(self.working_hours.is_open)

# # 
# def test_time_field_validation(self):
#     # Test that from_time and to_time accept valid time values
#     self.time.from_time = "09:00"
#     self.time.to_time = "22:00"
#     self.time.save()
#     # Convert string to datetime.time object before calling strftime
#     from_time_obj = datetime.strptime(self.time.from_time, "%H:%M").time()
#     to_time_obj = datetime.strptime(self.time.to_time, "%H:%M").time()
#     self.assertEqual(from_time_obj.strftime("%H:%M"), "09:00")
#     self.assertEqual(to_time_obj.strftime("%H:%M"), "22:00")
    
# class FacilitiesModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Setup test data used by all test methods
#         club = Club.objects.create(property_name="Test Club", country="Test Country")
#         User.objects.create_owner(
#             username="testuser",
#             email="testuser@test.com",
#             password="12345",
#         )
#         user = User.objects.get(username="testuser")
#         cls.branch = Branch.objects.create(
#             owner=user, club=club, address="Test Address"
#         )
#         cls.facility = Facilities.objects.create(
#             name="Gym",
#             icon="path/to/icon.png",
#             branch=cls.branch,
#         )

#     def test_name_label(self):
#         field_label = self.facility._meta.get_field('name').verbose_name
#         self.assertEqual(field_label, 'name')

#     def test_name_max_length(self):
#         max_length = self.facility._meta.get_field('name').max_length
#         self.assertEqual(max_length, 255)

#     def test_icon_upload_path(self):
#         upload_path = self.facility._meta.get_field('icon').upload_to
#         self.assertTrue(callable(upload_path))

#     def test_branch_label(self):
#         field_label = self.facility._meta.get_field('branch').verbose_name
#         self.assertEqual(field_label, 'branch')

#     def test_str_method(self):
#         expected_object_name = self.facility.name
#         self.assertEqual(str(self.facility), expected_object_name)