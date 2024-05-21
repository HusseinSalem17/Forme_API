import datetime
import os
from rest_framework import status
from rest_framework.response import Response
import base64
from django.core.files.base import ContentFile


def calculate_end_date(duration, start_date):
    # Convert the start date to a datetime object
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

    # Calculate the end date by adding the duration (in months) to the start date
    end_date = start_date + datetime.timedelta(days=30 * duration)

    # Convert the end date back to a string in the format "YYYY-MM-DD"
    end_date_str = end_date.strftime("%Y-%m-%d")

    return end_date_str


def flatten_errors(errors):
    flattened_errors = []
    non_field_errors = errors.pop("non_field_errors", None)
    for field, messages in errors.items():
        if isinstance(messages, dict):  # Check if the error is nested
            errors = {**errors, **messages}
            errors.pop(field)
            for key, value in messages.items():
                flattened_errors.append(" ".join(str(message) for message in value))
        else:
            flattened_errors.append(" ".join(str(message) for message in messages))
    if non_field_errors is not None:
        flattened_errors.append(" ".join(non_field_errors))
    return " ".join(flattened_errors)


# def flatten_errors(errors):
#     flattened_errors = {}
#     non_field_errors = errors.pop("non_field_errors", None)
#     for field, messages in errors.items():
#         if isinstance(messages, dict):  # Check if the error is nested
#             errors = {**errors, **messages}
#             errors.pop(field)
#             for key, value in messages.items():
#                 flattened_errors[key] = " ".join(str(message) for message in value)
#         else:
#             flattened_errors[field] = " ".join(str(message) for message in messages)
#     if non_field_errors is not None:
#         flattened_errors["non_field_errors"] = " ".join(non_field_errors)
#     return flattened_errors


def handle_validation_error(e):
    errors = e.detail
    print("errors here", errors)
    flattened_errors = flatten_errors(errors)
    return Response({"error": flattened_errors}, status=status.HTTP_400_BAD_REQUEST)


def base64_file(data, name=None):
    _format, _img_str = data.split(";base64,")
    _name, ext = _format.split("/")
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(
        base64.b64decode(_img_str), name="club_documents/{}.{}".format(name, ext)
    )


def get_file_path(folder, name, filename):
    # Create the folder path with the name
    folder_path = f"{folder}/{name}/"
    # Return the full file path
    return os.path.join(folder_path, filename)
