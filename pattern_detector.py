
import logging
from collections import Counter

logger = logging.getLogger(__name__)



def load_common_passwords(filepath: str = "common_passwords.txt") -> set:

    with open(filepath, encoding="utf-8", errors="ignore") as fh:
        return {line.strip().lower() for line in fh if line.strip()}


# Backwards-compat alias (old camelCase name)
def loadCommonPasswords(filepath: str = "common_passwords.txt") -> set:  # noqa: N802
    return load_common_passwords(filepath)



def common_password_checker(password: str, common_passwords: set) -> bool:
    """Return True if *password* (case-insensitive) is in *common_passwords*."""
    return password.lower() in common_passwords


def commonPasswordChecker(password: str, common_passwords: set) -> bool:  # noqa: N802
    return common_password_checker(password, common_passwords)


def pattern_checker(password: str) -> bool:
    """Return True if any single character appears 4 or more times."""
    counts = Counter(password.lower())
    return any(v >= 4 for v in counts.values())


def is_weak_password(password: str, common_passwords: set) -> bool:
    """Return True if the password is considered weak by any heuristic."""
    if common_password_checker(password, common_passwords):
        logger.debug("Password matched common-password list.")
        return True
    if pattern_checker(password):
        logger.debug("Password has a character repeated 4+ times.")
        return True
    return False


def isWeakPassword(password: str, common_passwords: set) -> bool:  # noqa: N802
    return is_weak_password(password, common_passwords)



if __name__ == "__main__":
    _common = load_common_passwords()
    print(is_weak_password("Password123", _common))  
    print(is_weak_password("Xk9$mQ2z!V3r", _common))  