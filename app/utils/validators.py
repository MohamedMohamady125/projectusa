"""
Validation utilities for various data types.
"""
import re
from datetime import date, datetime
from typing import Optional
from uuid import UUID


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid email format
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format (international format).

    Args:
        phone: Phone number to validate

    Returns:
        True if valid phone format
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    # Check if it contains only digits and optional + prefix
    phone_pattern = r'^\+?[0-9]{10,15}$'
    return bool(re.match(phone_pattern, cleaned))


def validate_gpa(gpa: float) -> bool:
    """
    Validate GPA value.

    Args:
        gpa: GPA value to validate

    Returns:
        True if valid GPA (0.0 to 4.0)
    """
    return 0.0 <= gpa <= 4.0


def validate_sat_score(score: int) -> bool:
    """
    Validate SAT score.

    Args:
        score: SAT score to validate

    Returns:
        True if valid SAT score (400 to 1600)
    """
    return 400 <= score <= 1600


def validate_act_score(score: int) -> bool:
    """
    Validate ACT score.

    Args:
        score: ACT score to validate

    Returns:
        True if valid ACT score (1 to 36)
    """
    return 1 <= score <= 36


def validate_toefl_score(score: int) -> bool:
    """
    Validate TOEFL score.

    Args:
        score: TOEFL score to validate

    Returns:
        True if valid TOEFL score (0 to 120)
    """
    return 0 <= score <= 120


def validate_graduation_date(graduation_date: date) -> bool:
    """
    Validate graduation date is in the future.

    Args:
        graduation_date: Graduation date to validate

    Returns:
        True if date is in the future
    """
    return graduation_date > date.today()


def validate_date_of_birth(dob: date, min_age: int = 13, max_age: int = 30) -> bool:
    """
    Validate date of birth is within acceptable range.

    Args:
        dob: Date of birth to validate
        min_age: Minimum age requirement
        max_age: Maximum age requirement

    Returns:
        True if age is within range
    """
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return min_age <= age <= max_age


def validate_swimming_time(time_seconds: float, event: str) -> bool:
    """
    Validate swimming time is realistic for the event.

    Args:
        time_seconds: Time in seconds
        event: Event name

    Returns:
        True if time is realistic
    """
    # Define reasonable time ranges for different events (in seconds)
    time_ranges = {
        "50": (15, 60),
        "100": (35, 150),
        "200": (80, 300),
        "400": (180, 600),
        "500": (220, 700),
        "800": (400, 1200),
        "1000": (500, 1500),
        "1500": (750, 2400),
        "1650": (800, 2500),
    }

    # Extract distance from event name
    distance = ''.join(filter(str.isdigit, event.split()[0]))

    if distance in time_ranges:
        min_time, max_time = time_ranges[distance]
        return min_time <= time_seconds <= max_time

    return True  # Allow if we don't have specific range


def validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL to validate

    Returns:
        True if valid URL format
    """
    url_pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$'
    return bool(re.match(url_pattern, url))


def validate_uuid(uuid_string: str) -> bool:
    """
    Validate UUID format.

    Args:
        uuid_string: UUID string to validate

    Returns:
        True if valid UUID format
    """
    try:
        UUID(uuid_string)
        return True
    except (ValueError, AttributeError):
        return False


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """
    Validate file extension.

    Args:
        filename: Filename to validate
        allowed_extensions: List of allowed extensions

    Returns:
        True if file extension is allowed
    """
    extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    return extension in [ext.lower() for ext in allowed_extensions]


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove potentially dangerous characters.

    Args:
        filename: Filename to sanitize

    Returns:
        Sanitized filename
    """
    # Remove path separators and dangerous characters
    filename = re.sub(r'[/\\<>:"|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename
