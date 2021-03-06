#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui.plugins.metrics import perfometer_info

perfometer_info.append({
    'type': 'dual',
    'perfometers': [{
        'type': 'logarithmic',
#        'segments': ['incoming_calls'],
        "metric": "incoming_calls",
        "half_value": 5,
        "exponent": 2.0,
    }, {
        'type': 'logarithmic',
#        'segments': ['outgoing_calls'],
        "metric": "outgoing_calls",
        "half_value": 5,
        "exponent": 2.0,
    }],
})
