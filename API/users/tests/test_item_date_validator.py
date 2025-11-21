from datetime import date, datetime

import pytest
from django.core.exceptions import ValidationError

from users.utils.validators import (
    MIN_ACCEPTABLE_DATE,
    validate_date_not_too_old,
)


def test_rejects_too_old_date():
    old = date(1830, 4, 19)
    with pytest.raises(ValidationError):
        validate_date_not_too_old(old)


def test_accepts_limit_date():
    limit = MIN_ACCEPTABLE_DATE
    # não deve falhar
    validate_date_not_too_old(limit)


def test_accepts_datetime_object():
    dt = datetime(1900, 1, 1, 12, 0, 0)
    validate_date_not_too_old(dt)

