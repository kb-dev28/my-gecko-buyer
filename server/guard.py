"""Refuse any RPC URL that is not a public HTTPS address."""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse


def is_public_url(url: str) -> bool:
    """True only for https URLs whose host is a public, globally routable address.

    If the name does not resolve, return False: a check server must not fetch a host
    it cannot prove is public. An unresolved name is not a public address.
    """
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return False
    host = parsed.hostname
    if not host:
        return False
    if host.casefold() in {"localhost", "localhost.localdomain"}:
        return False
    try:
        infos = socket.getaddrinfo(host, None)
    except OSError:
        return False
    if not infos:
        return False
    for info in infos:
        try:
            ip = ipaddress.ip_address(info[4][0])
        except ValueError:
            return False
        if not ip.is_global:
            return False
    return True
