from collections import Counter

def loadCommonPasswords(filepath="common_passwords.txt"):
    with open(filepath) as file:
        return {line.strip().lower() for line in file}

def commonPasswordChecker(password, common_passwords):
    if password.lower() in common_passwords:
        print("This is a commonly used password.")
        return True
    return False

def patternChecker(password):
    lowPassword = password.lower()
    counts = Counter(lowPassword)
    return any(v >= 4 for v in counts.values())

def isWeakPassword(password, common_passwords):
    if commonPasswordChecker(password, common_passwords):
        return True
    if patternChecker(password):
        print("This password has a character repeated 4+ times.")
        return True
    return False


common_passwords = loadCommonPasswords()


print(isWeakPassword("Password123", common_passwords))
print(isWeakPassword("Xk9$mQ2z", common_passwords))