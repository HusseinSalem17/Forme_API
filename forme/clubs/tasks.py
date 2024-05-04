# tasks.py

from celery import shared_task
from datetime import timezone

from .models import Attendance, MemberSubscription


@shared_task
def create_daily_attendance(member_subscription_id):
    try:
        member_subscription = MemberSubscription.objects.get(id=member_subscription_id)
        start_date = member_subscription.start_date
        end_date = member_subscription.end_date

        # Check if the current date is within the subscription period
        current_date = timezone.now().date()
        if start_date <= current_date <= end_date:
            # Check if attendance record for the current date already exists
            if not Attendance.objects.filter(
                branch_member=member_subscription, date=current_date
            ).exists():
                # Create attendance record for the current date
                Attendance.objects.create(
                    branch_member=member_subscription, date=current_date
                )
    except MemberSubscription.DoesNotExist:
        pass
