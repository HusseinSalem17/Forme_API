import datetime
from rest_framework.permissions import BasePermission
from rest_framework import status
from rest_framework.response import Response


def calculate_end_date(duration, start_date):
    # Convert the start date to a datetime object
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

    # Calculate the end date by adding the duration (in months) to the start date
    end_date = start_date + datetime.timedelta(days=30 * duration)

    # Convert the end date back to a string in the format "YYYY-MM-DD"
    end_date_str = end_date.strftime("%Y-%m-%d")

    return end_date_str


def flatten_errors(errors):
    flattened_errors = {}
    non_field_errors = errors.pop("non_field_errors", None)
    for field, messages in errors.items():
        if isinstance(messages, dict):  # Check if the error is nested
            errors = {**errors, **messages}
            errors.pop(field)
            for key, value in messages.items():
                flattened_errors[key] = " ".join(str(message) for message in value)
        else:
            flattened_errors[field] = " ".join(str(message) for message in messages)
    if non_field_errors is not None:
        flattened_errors["non_field_errors"] = " ".join(non_field_errors)
    return flattened_errors

def handle_validation_error(e):
    errors = e.detail
    flattened_errors = flatten_errors(errors)
    return Response({"error": flattened_errors}, status=status.HTTP_400_BAD_REQUEST)
