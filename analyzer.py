

import re


def analyze_password(password: str) -> dict:

    length = len(password)

    has_upper   = bool(re.search(r"[A-Z]",       password))
    has_lower   = bool(re.search(r"[a-z]",       password))
    has_digit   = bool(re.search(r"[0-9]",       password))
    has_special = bool(re.search(r"[^A-Za-z0-9]", password))

    points = 0

    if length >= 16:
        points += 4
    elif length >= 12:
        points += 3
    elif length >= 8:
        points += 2
    elif length >= 6:
        points += 1


    if has_upper:
        points += 1
    if has_lower:
        points += 1
    if has_digit:
        points += 1
    if has_special:
        points += 1


    if points >= 8:
        label = "strongest"
    elif points >= 6:
        label = "strong"
    elif points >= 4:
        label = "moderate"
    else:
        label = "weak"

    return {
        "length":     length,
        "hasUpper":   has_upper,
        "hasLower":   has_lower,
        "hasDigit":   has_digit,
        "hasSpecial": has_special,
        "points":     points,
        "label":      label,
    }



def ananlyze_password(password: str) -> dict:  
    return analyze_password(password)