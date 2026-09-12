

import hashlib
import logging
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

_TIMEOUT_SECS = 5        # network timeout per attempt
_MAX_RETRIES  = 2        # total retry attempts on transient errors
_RETRY_DELAY  = 0.5      # seconds between retries
_API_BASE     = "https://api.pwnedpasswords.com/range/"
_USER_AGENT   = "PasswordStrengthChecker/2.0 (educational project)"


def check_breach(password: str) -> int | str:
   
    sha1  = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url   = _API_BASE + prefix

    last_exc: Exception | None = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            req = Request(url, headers={"User-Agent": _USER_AGENT, "Add-Padding": "true"})
            with urlopen(req, timeout=_TIMEOUT_SECS) as resp:
                if resp.status != 200:
                    logger.warning("HIBP API returned HTTP %s", resp.status)
                    return "error"
                body = resp.read().decode("utf-8")
            break
        except (HTTPError, URLError, OSError) as exc:
            last_exc = exc
            logger.warning("HIBP request attempt %d failed: %s", attempt, exc)
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)
    else:
        logger.error("All HIBP retries exhausted: %s", last_exc)
        return "error"

    for line in body.splitlines():
        if not line.strip():
            continue
        parts = line.split(":")
        if len(parts) < 2:
            continue
        hash_suffix, count_str = parts[0], parts[1]
        if hash_suffix == suffix:
            return int(count_str)

    return 0


def check_breach_flag(password: str) -> bool | None:
   
    result = check_breach(password)
    if result == "error":
        return None
    return result > 0