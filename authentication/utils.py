from forme.utils import get_file_path, sanitize_path_component


def get_upload_path_user(instance, filename):
    # Use the sanitize_path_component function to sanitize the username
    safe_username = sanitize_path_component(instance.username)
    
    # Define the folder dynamically based on the instance's role
    if instance.is_owner():
        folder = "clubs/"
    elif instance.is_admin():
        folder = "admins/"
    elif instance.is_trainer():
        folder = "trainers/"
    elif instance.is_trainee():
        folder = "trainees/"
    else:
        folder = "users/"
    
    folder += f"{safe_username}"  # Use sanitized username
    type = "profile_pics"
    # Call get_file_path with the sanitized folder, type, and filename
    return get_file_path(folder, type, filename)