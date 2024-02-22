import os
from typing import Optional, List, Union, Dict
from uuid import UUID

from pydantic import BaseModel, Field

from .protocols import PROTOCOLS
from .trace import Trace

PYDANTIC_EXTRAS = os.getenv("IPFABRIC_PYDANTIC_EXTRAS", "allow")


class Extra(BaseModel, extra=PYDANTIC_EXTRAS):
    ip: Optional[str] = None


class Line(BaseModel, extra=PYDANTIC_EXTRAS):
    pattern: Optional[str] = None
    color: Optional[int] = None
    thickness: Optional[int] = None


class Style(BaseModel, extra=PYDANTIC_EXTRAS):
    background: Optional[str] = None
    line: Optional[Line] = None


class Position(BaseModel, extra=PYDANTIC_EXTRAS):
    x: Union[int, float]
    y: Union[int, float]


class EdgePosition(BaseModel, extra=PYDANTIC_EXTRAS):
    c: Position
    e: Position


class Label(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Optional[str] = None
    visible: Optional[bool] = None
    text: Optional[str] = None
    angle: Optional[int] = None
    anchor: Optional[Position] = None
    position: Optional[Position] = None


class Labels(BaseModel, extra=PYDANTIC_EXTRAS):
    center: Optional[Union[List[Label], Label]] = None
    source: Optional[Union[List[Label], Label]] = None
    target: Optional[Union[List[Label], Label]] = None


class ArrowHeads(BaseModel, extra=PYDANTIC_EXTRAS):
    target: Optional[List[Position]] = Field(default_factory=list)
    source: Optional[List[Position]] = Field(default_factory=list)


class Positions(BaseModel, extra=PYDANTIC_EXTRAS):
    line: Optional[List[Union[Position, EdgePosition]]] = Field(default_factory=list)
    arrowHeads: Optional[ArrowHeads] = None
    labels: Optional[Labels] = None


class Checks(BaseModel, extra=PYDANTIC_EXTRAS):
    green: int = Field(alias="0")
    blue: int = Field(alias="10")
    amber: int = Field(alias="20")
    red: int = Field(alias="30")


class Severity(Checks, extra=PYDANTIC_EXTRAS):
    pass


class Topics(BaseModel, extra=PYDANTIC_EXTRAS):
    acl: Checks = Field(alias="ACL")
    forwarding: Checks = Field(alias="FORWARDING")
    zonefw: Checks = Field(alias="ZONEFW")
    nat44: Optional[Checks] = Field(None, alias="NAT44")
    pbr: Optional[Checks] = Field(None, alias="PBR")


class TrafficScore(BaseModel, extra=PYDANTIC_EXTRAS):
    accepted: int
    dropped: int
    forwarded: int
    total: int


class Packets(BaseModel, extra=PYDANTIC_EXTRAS):
    packet: Optional[List[PROTOCOLS]] = Field(default_factory=list)
    ifaceName: Optional[str] = None
    prevEdgeIds: Optional[List[str]] = Field(default_factory=list)
    nextEdgeIds: Optional[List[str]] = Field(default_factory=list)
    severityInfo: Optional[Checks] = None
    trafficScore: Optional[TrafficScore] = None


class Node(BaseModel, extra=PYDANTIC_EXTRAS):
    path: Optional[str] = None
    boxId: Optional[str] = None
    children: List
    graphType: str
    id: str
    label: str
    parentPath: Optional[str] = None
    sn: str
    type: str
    stack: Optional[bool] = None
    position: Optional[Position] = None
    style: Optional[Style] = None
    acceptedPackets: Optional[Dict[str, Packets]] = Field(default_factory=dict)
    droppedPackets: Optional[Dict[str, Packets]] = Field(default_factory=dict)
    generatedPackets: Optional[Dict[str, Packets]] = Field(default_factory=dict)
    extra: Optional[Extra] = None


class Edge(BaseModel, extra=PYDANTIC_EXTRAS):
    direction: str
    source: str
    target: str
    edgeSettingsId: UUID
    id: str
    labels: Labels
    protocol: Optional[str] = ""
    shift: Optional[Union[int, float]] = None
    positions: Optional[Positions] = None
    style: Optional[Style] = None


class NetworkEdge(Edge, BaseModel, extra=PYDANTIC_EXTRAS):
    circle: bool
    children: List[str]


class PathLookupEdge(Edge, BaseModel, extra=PYDANTIC_EXTRAS):
    nextEdgeIds: List[str]
    prevEdgeIds: List[str]
    packet: List[PROTOCOLS]
    severityInfo: Severity
    sourceIfaceName: Optional[str] = None
    targetIfaceName: Optional[str] = None
    trafficScore: TrafficScore
    nextEdge: Optional[list] = Field(default_factory=list)
    prevEdge: Optional[list] = Field(default_factory=list)


class EventsSummary(BaseModel, extra=PYDANTIC_EXTRAS):
    flags: list
    topics: Topics
    global_list: list = Field(alias="global")


class Traces(BaseModel, extra=PYDANTIC_EXTRAS):
    severityInfo: Checks
    sourcePacketId: str
    targetPacketId: str
    trace: List[Trace]


class Decision(BaseModel, extra=PYDANTIC_EXTRAS):
    traces: List[Traces]
    trafficIn: Optional[Dict[str, List[str]]] = Field(default_factory=dict)
    trafficOut: Optional[Dict[str, List[str]]] = Field(default_factory=dict)


class Check(BaseModel, extra=PYDANTIC_EXTRAS):
    exists: bool


class PathLookup(BaseModel, extra=PYDANTIC_EXTRAS):
    eventsSummary: EventsSummary
    decisions: Dict[str, Decision]
    passingTraffic: str
    check: Check


class GraphResult(BaseModel, extra=PYDANTIC_EXTRAS):
    nodes: Dict[str, Node]
    edges: Dict[str, Union[NetworkEdge, PathLookupEdge]]
    pathlookup: Optional[PathLookup] = None
