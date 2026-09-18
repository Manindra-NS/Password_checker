
import logging
from collections import Counter

logger = logging.getLogger(__name__)


def load_common_passwords(filepath: str = "common_passwords.txt") -> set:
    with open(filepath, encoding="utf-8", errors="ignore") as fh:
        return {line.strip().lower() for line in fh if line.strip()}

def loadCommonPasswords(filepath: str = "common_passwords.txt") -> set: 
    return load_common_passwords(filepath)

def common_password_checker(password: str, common_passwords: set) -> bool:
    return password.lower() in common_passwords

def commonPasswordChecker(password: str, common_passwords: set) -> bool:  
    return common_password_checker(password, common_passwords)

def pattern_checker(password: str) -> bool:
    counts = Counter(password.lower())
    return any(v >= 4 for v in counts.values())

def is_weak_password(password: str, common_passwords: set) -> bool:
    if common_password_checker(password, common_passwords):
        logger.debug("Password matched common-password list.")
        return True
    if pattern_checker(password):
        logger.debug("Password has a character repeated 4+ times.")
        return True
    return False


def isWeakPassword(password: str, common_passwords: set) -> bool: 
    return is_weak_password(password, common_passwords)

 