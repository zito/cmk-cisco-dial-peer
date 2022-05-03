#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersApplications,
)
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    TextAscii,
    Tuple,
)


def _item_spec_line():
    return TextAscii(title=_("Line number"), allow_empty=False)


def _parameter_valuespec_line():
    return Dictionary(elements=[
        ("incoming_call_levels",
            Tuple(
                title=_("Incoming Call levels"),
                elements=[
                    Integer(title=_("Warning at"), unit=_("calls")),
                    Integer(title=_("Critical at"), unit=_("calls")),
                ],
            ),
        ),
        ("outgoing_call_levels",
            Tuple(
                title=_("Outgoing Call levels"),
                elements=[
                    Integer(title=_("Warning at"), unit=_("calls")),
                    Integer(title=_("Critical at"), unit=_("calls")),
                ],
            ),
        ),
    ])


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="cisco_dial_peer",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_line,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_line,
        title=lambda: _("Cisco Dial Peer"),
    ))
