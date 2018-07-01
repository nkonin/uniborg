# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

from dotenv import load_dotenv
from uniborg import Uniborg
from uniborg.util import get_proxy

logging.basicConfig(level=logging.INFO)

load_dotenv()

borg = Uniborg("stdborg", plugin_path="stdplugins", connection_retries=None, proxy=get_proxy())

borg.run_until_disconnected()
