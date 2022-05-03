#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.i18n import _
from cmk.gui.plugins.metrics import metric_info

metric_info["incoming_calls"] = {
    "title": _("Incoming Calls"),
    "unit": "count",
    "color": "15/a",
}

metric_info["outgoing_calls"] = {
    "title": _("Outgoing Calls"),
    "unit": "count",
    "color": "24/a",
}
