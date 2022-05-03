#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:sta:si:sw=4:sts=4:et:

from .agent_based_api.v1 import (
        check_levels,
        exists,
        Metric,
        OIDEnd,
        register,
        render,
        Result,
        Service,
        SNMPTree,
        State
    )
from .agent_based_api.v1.type_defs import CheckResult, DiscoveryResult, StringTable
from typing import Any, Dict


CHECK_DEFAULT_PARAMETERS = {
    'incoming_call_levels': (50, 60),
    'outgoing_call_levels': (50, 60),
}


Section = Dict[str, Any]

def parse_cisco_dial_peer(string_table: StringTable) -> Section:

    def row_status_text(status):
        return {
                1: "active",
                2: "not in service",
                3: "not ready",
                }.get(int(status), "unknown")

    parsed = {}
    for num, status, in_calls, out_calls in string_table:
        parsed[num] = {
                "status": row_status_text(status),
                "in_calls": int(in_calls),
                "out_calls": int(out_calls),
                }
    return parsed

def discover_cisco_dial_peer(section: Section) -> DiscoveryResult:
    for key in section.keys():
        if section[key]["status"] == "active":
            yield Service(item=key)
 
def check_cisco_dial_peer(item: str, params: Dict[str, Any], section: Section) -> CheckResult:
    if item in section:
        d = section[item]
        status = d["status"]
        in_calls = d["in_calls"]
        out_calls = d["out_calls"]
        state = State.OK if status == "active" else State.CRIT
        yield Result(state = state, summary = f"Status: {status}")
        yield from check_levels(in_calls,
                    metric_name = 'incoming_calls',
                    levels_upper = params.get('incoming_call_levels'),
                    render_func = lambda x: f"{x}",
                    label = 'Incoming Calls')
        yield from check_levels(out_calls,
                    metric_name = 'outgoing_calls',
                    levels_upper = params.get('outgoing_call_levels'),
                    render_func = lambda x: f"{x}",
                    label = 'Outgoing Calls')


register.snmp_section(
    name = "cisco_dial_peer",
    detect = exists(".1.3.6.1.4.1.9.9.63.*"),  # CISCO-VOICE-DIAL-CONTROL-MIB::ciscoVoiceDialControlMIB
    fetch = SNMPTree(
        base = ".1.3.6.1.4.1.9.9.63.1",    # CISCO-VOICE-DIAL-CONTROL-MIB::cvdcMIBObjects
        oids = [
            OIDEnd(),
            "2.1.1.4",    # CISCO-VOICE-DIAL-CONTROL-MIB::cvPeerCfgRowStatus
            "3.8.4.1.1",  # CISCO-VOICE-DIAL-CONTROL-MIB::cvCallVolPeerIncomingCalls
            "3.8.4.1.2",  # CISCO-VOICE-DIAL-CONTROL-MIB::cvCallVolPeerOutgoingCalls
        ],
    ),
    parse_function = parse_cisco_dial_peer,
)

register.check_plugin(
    name = "cisco_dial_peer",
    service_name = "Dial Peer %s",
    check_function = check_cisco_dial_peer,
    check_default_parameters = CHECK_DEFAULT_PARAMETERS,
    discovery_function = discover_cisco_dial_peer,
    check_ruleset_name = "cisco_dial_peer",
)
