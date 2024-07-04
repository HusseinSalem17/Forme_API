import datetime
import os
from rest_framework import status
from rest_framework.response import Response
import base64
from django.core.files.base import ContentFile

from forme.utils import get_file_path, sanitize_path_component


def calculate_end_date(duration, start_date):
    # Convert the start date to a datetime object
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

    # Calculate the end date by adding the duration (in months) to the start date
    end_date = start_date + datetime.timedelta(days=30 * duration)

    # Convert the end date back to a string in the format "YYYY-MM-DD"
    end_date_str = end_date.strftime("%Y-%m-%d")

    return end_date_str


# def base64_file(data, name=None):
#     _format, _img_str = data.split(";base64,")
#     _name, ext = _format.split("/")
#     if not name:
#         name = _name.split(":")[-1]
#     return ContentFile(
#         base64.b64decode(_img_str), name="club_documents/{}.{}".format(name, ext)
#     )


def base64_file(data, name=None):
    _format, _img_str = data.split(';base64,')
    _name, ext = _format.split('/')
    if not name:
        name = _name.split(":")[-1]
    return ContentFile(base64.b64decode(_img_str), name='{}.{}'.format(name, ext))

def get_upload_path_for_branch_gallery(instance, filename):
    # Use the sanitize_path_component function to sanitize the property_name
    safe_property_name = sanitize_path_component(instance.branch.club.property_name)

    folder = f"branches/{safe_property_name}"  # Use sanitized property name
    type = "branch_gallery"
    return get_file_path(folder, type, filename)


def get_upload_path_forl_club_icon_facility(instance, filename):
    folder = f"/clubs/{instance.club.property_name}/facilities"
    type = "club_icons"
    return get_file_path(folder, type, filename)


def get_upload_path_for_club_documents(instance, filename):
    folder = f"/clubs/{instance.club.property_name}"
    type = "club_documents"
    return get_file_path(folder, type, filename)


def get_upload_path_new_trainers(instance, filename):
    folder = f"new_trainers/{instance.username}"
    type = "profile_pics"
    return get_file_path(folder, type, filename)
