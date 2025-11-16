"""
Input validation utilities for production
"""
import re
from decimal import Decimal, InvalidOperation

def validate_telegram_user_id(user_id):
    """Validate Telegram user ID"""
    try:
        uid = int(user_id)
        return 1 <= uid <= 2**63 - 1
    except (ValueError, TypeError):
        return False

def validate_username(username):
    """Validate username format"""
    if not username:
        return True  # Username is optional
    if len(username) > 255:
        return False
    # Telegram usernames: 5-32 chars, alphanumeric and underscores
    return bool(re.match(r'^[a-zA-Z0-9_]{5,32}$', username))

def validate_probability(prob):
    """Validate probability value (0-1)"""
    try:
        p = Decimal(str(prob))
        return Decimal('0') <= p <= Decimal('1')
    except (ValueError, InvalidOperation, TypeError):
        return False

def validate_positive_integer(value):
    """Validate positive integer"""
    try:
        v = int(value)
        return v > 0
    except (ValueError, TypeError):
        return False

def sanitize_string(value, max_length=255):
    """Sanitize string input"""
    if not isinstance(value, str):
        return None
    # Remove null bytes and trim
    value = value.replace('\x00', '').strip()
    if len(value) > max_length:
        value = value[:max_length]
    return value

def validate_json_structure(data, required_fields=None, field_types=None):
    """Validate JSON structure"""
    if not isinstance(data, dict):
        return False
    
    if required_fields:
        for field in required_fields:
            if field not in data:
                return False
    
    if field_types:
        for field, expected_type in field_types.items():
            if field in data and not isinstance(data[field], expected_type):
                return False
    
    return True

