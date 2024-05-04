from rest_framework import renderers
import json


class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if isinstance(data, dict) and 'ErrorDetail' in str(data):
            errors = data.get('detail', {})
            # Flatten the error dictionary
            non_field_errors = errors.pop("non_field_errors", None)
            for field, messages in errors.items():
                if isinstance(messages, dict):  # Check if the error is nested
                    errors = {**errors, **messages}
                    errors.pop(field)
                    for key, value in messages.items():
                        errors[key] = " ".join(str(message) for message in value)
                else:
                    errors[field] = " ".join(str(message) for message in messages)
            if non_field_errors is not None:
                errors["non_field_errors"] = " ".join(non_field_errors)
            response = json.dumps({'errors': errors})
        else:
            response = json.dumps({'data': data})
        return response
