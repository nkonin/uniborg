# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os
import re
from urllib.parse import urlparse

import socks
from telethon import events
from telethon.tl.functions.messages import GetPeerDialogsRequest


def admin_cmd(pattern):
    return events.NewMessage(outgoing=True, pattern=re.compile(pattern))


async def is_read(borg, entity, message, is_out=None):
    """
    Returns True if the given message (or id) has been read
    if a id is given, is_out needs to be a bool
    """
    is_out = getattr(message, "out", is_out)
    if not isinstance(is_out, bool):
        raise ValueError(
            "Message was id but is_out not provided or not a bool")
    message_id = getattr(message, "id", message)
    if not isinstance(message_id, int):
        raise ValueError("Failed to extract id from message")

    dialog = (await borg(GetPeerDialogsRequest([entity]))).dialogs[0]
    max_id = dialog.read_outbox_max_id if is_out else dialog.read_inbox_max_id
    return message_id <= max_id


def get_proxy():
    # TODO add command-line arguments support
    proxy_str = os.getenv('PROXY')
    return parse_proxy_str(proxy_str)


def parse_proxy_str(proxy_str):
    """
    Returns proxy from given string
    """
    url_parser = urlparse(proxy_str)
    proxy_type = None
    proxy_type_str = url_parser.scheme

    if proxy_type_str.lower() == "socks5":
        proxy_type = socks.SOCKS5
    elif proxy_type_str.lower() == "socks4":
        proxy_type = socks.SOCKS4
    elif proxy_type_str.lower() == "https":
        proxy_type = socks.HTTP
    elif proxy_type_str.lower() == "http":
        proxy_type = socks.HTTP
    else:
        raise ValueError("Proxy type %s is not supported" % proxy_type)

    host = url_parser.hostname
    port = url_parser.port

    if host is None:
        raise ValueError("Host parsing error")
    if port is None:
        raise ValueError("Port parsing error")

    user = url_parser.username
    password = url_parser.password

    if user is not None and password is not None:
        proxy = (proxy_type, host, port, True, user, password)
    else:
        proxy = (proxy_type, host, port)
    return proxy
