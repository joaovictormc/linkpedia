from pydantic import ValidationError
from pydantic_core import InitErrorDetails

def create_validation_errors(instance, field_names, error_messages):
    if hasattr(instance, "dict"):
        values = instance.dict()
    else:
        values = instance  # Assuming instance is already a dictionary

    validation_errors = []
    for field_name, error_message in zip(field_names, error_messages):
        error_detail = InitErrorDetails(
            {
                "type": "value_error",
                "loc": ["body", field_name],
                "input": values.get(field_name),
                "ctx": {
                    "error": f"{error_message}",
                },
            }
        )
        validation_errors.append(error_detail)
    errors_obj = ValidationError.from_exception_data(
        title="detail", line_errors=validation_errors
    )
    return {"detail": errors_obj.errors(include_input=False, include_url=False)}
