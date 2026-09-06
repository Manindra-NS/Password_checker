import hashlib
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def check_breach(password):

    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()

    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        request = Request(url, headers={"User-Agent": "PasswordChecker/1.0"})
        with urlopen(request) as response:
            if response.status != 200:
                return "Unable to check breach status"
            response_text = response.read().decode("utf-8")
    except (HTTPError, URLError):
        return "Unable to check breach status"

    hashes = response_text.splitlines()

    for line in hashes:
        hash_suffix, count = line.split(":")

        if hash_suffix == suffix:
            return int(count)

    return 0

def check_breach_flag(password):
    result = check_breach(password)

    if result == "Unable to check breach status":
        return None  
    elif result > 0:
        return True   
    else:
        return False  