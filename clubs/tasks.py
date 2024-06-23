# tasks.py

from celery import shared_task
from datetime import timezone

from clubs.models import Time

from .models import Attendance, Branch, MemberSubscription

from forme.celery import app

@shared_task
# def create_daily_attendance(member_subscription_id):
#     try:
#         member_subscription = MemberSubscription.objects.get(id=member_subscription_id)
#         start_date = member_subscription.start_date
#         end_date = member_subscription.end_date

#         # Check if the current date is within the subscription period
#         current_date = timezone.now().date()
#         if start_date <= current_date <= end_date:
#             # Check if attendance record for the current date already exists
#             if not Attendance.objects.filter(
#                 branch_member=member_subscription, date=current_date
#             ).exists():
#                 # Create attendance record for the current date
#                 Attendance.objects.create(
#                     branch_member=member_subscription, date=current_date
#                 )
#     except MemberSubscription.DoesNotExist:
#         pass


@app.task(name="update_is_open")
def update_is_open():
    now = timezone.now().time()
    for time in Time.objects.all():
        if time.from_time <= now <= time.to_time:
            time.day.is_open = True
            time.day.branch.is_open = True
        else:
            time.day.is_open = False
            time.day.branch.is_open = False
        time.day.save()
        time.day.branch.save()
        
        
@shared_task
def decrease_new_members(branch_id):
    branch = Branch.objects.get(id=branch_id)
    if branch.new_members > 0:
        branch.new_members -= 1
        branch.save()