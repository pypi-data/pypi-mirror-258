from enum import Enum
from pydantic import Field


class ProtocolController(str, Enum):
    icmp = "icmp"
    igmp = "igmp"
    ggp = "ggp"
    vip_encap = "ip-encap"
    st = "st"
    tcp = "tcp"
    egp = "egp"
    pup = "pup"
    udp = "udp"
    hmp = "hmp"
    xns_idp = "xns-idp"
    rdp = "rdp"
    iso_tp4 = "iso-tp4"
    dccp = "dccp"
    xtp = "xtp"
    ddp = "ddp"
    idpr_cmtp = "idpr-cmtp"
    ipv6_encap = "ipv6-encap"
    rsvp = "rsvp"
    gre = "gre"
    ipsec_esp = "ipsec-esp"
    ipsec_ah = "ipsec-ah"
    rspf = "rspf"
    vmtp = "vmtp"
    ospf = "ospf"
    ipip = "ipip"
    etherip = "etherip"
    encap = "encap"
    pim = "pim"
    vrrp = "vrrp"
    l2tp = "l2tp"
    sctp = "sctp"
    udp_lite = "udp-lite"


protocol = Field(default=None)
