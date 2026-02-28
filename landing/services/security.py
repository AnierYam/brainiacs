import hashlib
import ipaddress
import re


_DEVICE_HEADERS = (
    "HTTP_USER_AGENT",
    "HTTP_ACCEPT_LANGUAGE",
    "HTTP_SEC_CH_UA",
    "HTTP_SEC_CH_UA_PLATFORM",
    "HTTP_SEC_CH_UA_MOBILE",
    "HTTP_SEC_CH_UA_MODEL",
)


def _normalize_header_value(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def _coerce_ip(value: str | None):
    if not value:
        return None
    candidate = value.strip()
    if not candidate:
        return None
    if candidate.startswith("[") and "]" in candidate:
        candidate = candidate[1 : candidate.index("]")]
    try:
        return ipaddress.ip_address(candidate)
    except ValueError:
        pass
    # Handle "ip:port" for IPv4 inputs.
    if ":" in candidate and "." in candidate and candidate.count(":") == 1:
        host = candidate.split(":", 1)[0].strip()
        try:
            return ipaddress.ip_address(host)
        except ValueError:
            return None
    return None


def _is_public_address(address) -> bool:
    return not (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    )


def build_device_hash(request) -> str:
    parts = []
    for header_name in _DEVICE_HEADERS:
        raw = request.META.get(header_name, "")
        parts.append(_normalize_header_value(raw))
    fingerprint = "|".join(parts)
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()


def summarize_user_agent(user_agent: str, limit: int = 140) -> str:
    cleaned = _normalize_header_value(user_agent)
    if len(cleaned) <= limit:
        return cleaned
    return f"{cleaned[: limit - 1]}..."


def get_client_ip(request) -> str:
    xff_raw = request.META.get("HTTP_X_FORWARDED_FOR", "")
    xff_addresses = []
    if xff_raw:
        for part in xff_raw.split(","):
            addr = _coerce_ip(part)
            if addr:
                xff_addresses.append(addr)
    if xff_addresses:
        for addr in xff_addresses:
            if _is_public_address(addr):
                return str(addr)
        return str(xff_addresses[0])
    remote_addr = _coerce_ip(request.META.get("REMOTE_ADDR"))
    if remote_addr:
        return str(remote_addr)
    return ""

