import os
from typing import List, Union, Optional, Literal

from pydantic import BaseModel, Field

try:
    from typing import Annotated  # py38 required Annotated
except ImportError:
    from typing_extensions import Annotated

PYDANTIC_EXTRAS = os.getenv("IPFABRIC_PYDANTIC_EXTRAS", "allow")


class Number(BaseModel, extra=PYDANTIC_EXTRAS):
    min: int
    max: int


class Numbers(BaseModel, extra=PYDANTIC_EXTRAS):
    """Possibly only for Internal Testing"""

    numbers: List[Number]


class Transport(BaseModel, extra=PYDANTIC_EXTRAS):
    src: Union[List[str], str]
    dst: Union[List[str], Numbers, str]


class TCP(Transport, BaseModel, extra=PYDANTIC_EXTRAS):
    flags: List[str]
    type: Literal["tcp"]


class UDP(Transport, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["udp"]


class ICMP(BaseModel, extra=PYDANTIC_EXTRAS):
    icmpCode: int
    icmpType: int
    type: Literal["icmp"]


class MPLS(BaseModel, extra=PYDANTIC_EXTRAS):
    stack: List[int]
    type: Literal["mpls"]


class Ethernet(BaseModel, extra=PYDANTIC_EXTRAS):
    src: Optional[str] = None
    dst: Optional[str] = None
    etherType: str
    type: Literal["ethernet"]
    vlan: Optional[int] = None


class ESP(BaseModel, extra=PYDANTIC_EXTRAS):
    payload: str
    nextHeader: str
    type: Literal["esp"]


class IP(BaseModel, extra=PYDANTIC_EXTRAS):
    src: List[str]
    dst: List[str]
    fragmentOffset: int = Field(alias="fragment offset")
    protocol: str
    ttl: int
    type: Literal["ip"]


class VXLAN(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["vxlan"]
    vni: int
    groupPolicyId: Optional[int] = None
    policyApplied: Optional[bool] = None


class CAPWAP(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["capwap"]


class GRE(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["gre"]
    protoType: Optional[str] = None


class FabricPath(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["fp"]
    dstSubswitchId: int
    dstSwitchId: int
    etherType: str
    srcSwitchId: int
    ttl: int


PROTOCOLS = Annotated[
    Union[ICMP, UDP, TCP, Ethernet, IP, MPLS, ESP, VXLAN, CAPWAP, GRE, FabricPath], Field(discriminator="type")
]
