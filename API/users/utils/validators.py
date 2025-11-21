from datetime import date
from django.core.exceptions import ValidationError

MIN_ACCEPTABLE_DATE = date(1900, 1, 1)

def validate_date_not_too_old(value):
    if value is None:
        return value

    try:
        value_date = value.date() if hasattr(value, "date") else value
    except Exception:
        return value

    if value_date < MIN_ACCEPTABLE_DATE:
        raise ValidationError(
            f"Data muito antiga. A data mínima permitida é {MIN_ACCEPTABLE_DATE.isoformat()}."
        )

    return value