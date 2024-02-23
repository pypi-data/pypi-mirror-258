import logging
from typing import Union, Dict, List, Optional, Literal
from warnings import warn

from ipfabric.api import IPFabricAPI
from .input_models.graph_parameters import Unicast, Multicast, Host2GW, Network
from .input_models.graph_settings import (
    NetworkSettings,
    PathLookupSettings,
    GraphSettings,
    Overlay,
    GroupSettings,
)
from .output_models.graph_result import NetworkEdge, Node, PathLookupEdge, GraphResult, PathLookup

logger = logging.getLogger("ipfabric")
WARNING = "This method will be removed in v6.9."
GRAPHS_URL = "graphs/"


class Diagram:
    def __init__(self, ipf):
        self.ipf = ipf

    def _check_graph_cache(self, snapshot_id):
        snapshot_id = snapshot_id or self.ipf.snapshot_id
        if snapshot_id not in self.ipf.loaded_snapshots:
            raise ValueError(f"Snapshot {snapshot_id} is not loaded or not found in IP Fabric.")
        if self.ipf.snapshots[snapshot_id].disabled_graph_cache:
            raise ValueError(f"Snapshot {snapshot_id} has Graph Cache tasks disabled.")
        return snapshot_id

    def _create_overlay(self, overlay: dict) -> Overlay:
        if overlay.get("intentRuleId", None):
            try:
                Overlay._valid_intentrule(overlay["intentRuleId"])
            except ValueError:
                if not self.ipf.intent.loaded:
                    self.ipf.intent.load_intent()
                intents = self.ipf.intent.intents_by_name[overlay["intentRuleId"]]
                if len(intents) > 1:
                    raise ValueError(f"Multiple Intents found with name `{overlay['intentRuleId']}`.")
                else:
                    overlay["intentRuleId"] = intents[0].intent_id
        return Overlay(**overlay)

    def _format_overlay(self, overlay: Union[Overlay, dict], snapshot_id: str = None) -> dict:
        if isinstance(overlay, dict):
            overlay = self._create_overlay(overlay)

        if overlay.type == "compare":
            self._check_graph_cache(overlay.snapshotToCompare)
            overlay.snapshotToCompare = self.ipf.snapshots[overlay.snapshotToCompare].snapshot_id
            if snapshot_id or self.ipf.snapshot_id == overlay.snapshotToCompare:
                raise ValueError(f"Cannot compare snapshot `{overlay.snapshotToCompare}` to itself.")
        return overlay.overlay()

    def _query(
        self,
        parameters: dict,
        snapshot_id: str = None,
        overlay: Union[Overlay, dict] = None,
        image: str = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
    ):
        """
        Submits a query, does no formatting on the parameters.  Use for copy/pasting from the webpage.
        :param parameters: dict: Dictionary to submit in POST.
        :return: list: List of Dictionary objects.
        """
        url = GRAPHS_URL + image if image else GRAPHS_URL
        payload = dict(parameters=parameters, snapshot=self._check_graph_cache(snapshot_id))
        if overlay:
            payload["overlay"] = self._format_overlay(overlay, snapshot_id)
        if graph_settings:
            payload["settings"] = graph_settings.settings()
        if attr_filters or self.ipf.attribute_filters:
            payload["attributeFilters"] = attr_filters or self.ipf.attribute_filters
        res = self.ipf.post(url, json=payload)
        res.raise_for_status()
        return res.content if image else res.json()

    def json(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Union[Overlay, dict] = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        unicast_swap_src_dst: bool = False,
    ) -> dict:
        return self._query(
            parameters.parameters(unicast_swap_src_dst) if isinstance(parameters, Unicast) else parameters.parameters(),
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            graph_settings=graph_settings,
        )

    def svg(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Union[Overlay, dict] = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        unicast_swap_src_dst: bool = False,
    ) -> bytes:
        return self._query(
            parameters.parameters(unicast_swap_src_dst) if isinstance(parameters, Unicast) else parameters.parameters(),
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            image="svg",
            graph_settings=graph_settings,
        )

    def png(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Union[Overlay, dict] = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        unicast_swap_src_dst: bool = False,
    ) -> bytes:
        return self._query(
            parameters.parameters(unicast_swap_src_dst) if isinstance(parameters, Unicast) else parameters.parameters(),
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            image="png",
            graph_settings=graph_settings,
        )

    def share_link(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Union[Overlay, dict] = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        unicast_swap_src_dst: bool = False,
    ) -> str:
        parameters = (
            parameters.parameters(unicast_swap_src_dst) if isinstance(parameters, Unicast) else parameters.parameters()
        )
        resp = self._query(
            parameters,
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            graph_settings=graph_settings,
        )

        parameters.pop("layouts", None)
        payload = {
            "graphView": {
                "name": "Shared view",
                "parameters": parameters,
                "collapsedNodeGroups": [],
                "hiddenNodes": [],
                "positions": {k: v["position"] for k, v in resp["graphResult"]["graphData"]["nodes"].items()},
                "settings": resp["graphResult"]["settings"],
            },
            "snapshot": self._check_graph_cache(snapshot_id),
        }
        if overlay:
            payload["graphView"]["overlay"] = self._format_overlay(overlay, snapshot_id)
        res = self.ipf.post("graphs/urls", json=payload)
        res.raise_for_status()
        return str(self.ipf.base_url.join(f"/diagrams/share/{res.json()['id']}"))

    def model(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        unicast_swap_src_dst: bool = False,
    ) -> GraphResult:
        json_data = self.json(parameters, snapshot_id, overlay, graph_settings, attr_filters, unicast_swap_src_dst)
        edge_setting_dict = self._diagram_edge_settings(json_data["graphResult"]["settings"])
        if isinstance(parameters, Network):
            return self._diagram_network(json_data, edge_setting_dict)
        else:
            return self._diagram_pathlookup(json_data, edge_setting_dict)

    @staticmethod
    def _diagram_network(json_data: dict, edge_setting_dict: dict, pathlookup: bool = False) -> GraphResult:
        edges, nodes = dict(), dict()
        for node_id, node in json_data["graphResult"]["graphData"]["nodes"].items():
            nodes[node_id] = Node.model_validate(node)

        for edge_id, edge_json in json_data["graphResult"]["graphData"]["edges"].items():
            edge = PathLookupEdge.model_validate(edge_json) if pathlookup else NetworkEdge.model_validate(edge_json)
            edge.protocol = (
                edge_setting_dict[edge.edgeSettingsId].name if edge.edgeSettingsId in edge_setting_dict else None
            )
            if edge.source:
                edge.source = nodes[edge.source]
            if edge.target:
                edge.target = nodes[edge.target]
            edges[edge_id] = edge

        return GraphResult(edges=edges, nodes=nodes)

    def _diagram_pathlookup(self, json_data: dict, edge_setting_dict: dict) -> GraphResult:
        graph_result = self._diagram_network(json_data, edge_setting_dict, pathlookup=True)

        for edge_id, edge in graph_result.edges.items():
            for prev_id in edge.prevEdgeIds:
                edge.prevEdge.append(graph_result.edges[prev_id])
            for next_id in edge.nextEdgeIds:
                edge.nextEdge.append(graph_result.edges[next_id] if next_id in graph_result.edges else next_id)
        graph_result.pathlookup = PathLookup.model_validate(json_data["pathlookup"])

        return graph_result

    @staticmethod
    def _diagram_edge_settings(graph_settings: dict) -> dict:
        net_settings = GraphSettings(**graph_settings)
        edge_setting_dict = dict()
        for edge in net_settings.edges:
            edge_setting_dict[edge.id] = edge
            if isinstance(edge, GroupSettings):
                for child in edge.children:
                    edge_setting_dict[child.id] = child
        return edge_setting_dict

    # TODO: Remove in v7.0
    def diagram_json(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        unicast_swap_src_dst: bool = False,
    ) -> dict:
        warn(f"{WARNING} Please use IPFClient().diagram.json()", DeprecationWarning, stacklevel=2)
        logger.warning(f"{WARNING} Please use IPFClient().diagram.json()")
        return self._query(
            parameters.parameters(unicast_swap_src_dst) if isinstance(parameters, Unicast) else parameters.parameters(),
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            graph_settings=graph_settings,
        )

    def diagram_svg(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        unicast_swap_src_dst: bool = False,
    ) -> bytes:
        warn(f"{WARNING} Please use IPFClient().diagram.svg()", DeprecationWarning, stacklevel=2)
        logger.warning(f"{WARNING} Please use IPFClient().diagram.json()")
        return self._query(
            parameters.parameters(unicast_swap_src_dst) if isinstance(parameters, Unicast) else parameters.parameters(),
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            image="svg",
            graph_settings=graph_settings,
        )

    def diagram_png(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        unicast_swap_src_dst: bool = False,
    ) -> bytes:
        warn(f"{WARNING} Please use IPFClient().diagram.png()", DeprecationWarning, stacklevel=2)
        logger.warning(f"{WARNING} Please use IPFClient().diagram.json()")
        return self._query(
            parameters.parameters(unicast_swap_src_dst) if isinstance(parameters, Unicast) else parameters.parameters(),
            snapshot_id=snapshot_id,
            overlay=overlay,
            attr_filters=attr_filters,
            image="png",
            graph_settings=graph_settings,
        )

    def diagram_model(
        self,
        parameters: Union[Unicast, Multicast, Host2GW, Network],
        snapshot_id: str = None,
        overlay: Overlay = None,
        graph_settings: Union[NetworkSettings, PathLookupSettings, GraphSettings] = None,
        attr_filters: Optional[Dict[str, List[str]]] = None,
        unicast_swap_src_dst: bool = False,
    ) -> GraphResult:
        warn(f"{WARNING} Please use IPFClient().diagram.json()", DeprecationWarning, stacklevel=2)
        logger.warning(f"{WARNING} Please use IPFClient().diagram.json()")
        return self.model(
            parameters,
            snapshot_id=snapshot_id,
            overlay=overlay,
            graph_settings=graph_settings,
            attr_filters=attr_filters,
            unicast_swap_src_dst=unicast_swap_src_dst,
        )

    def _graph_url(self, url_id: str, data: Literal["json", "code", "model", "svg", "png"] = "json"):
        query = self.ipf._get_shared_view(url_id, "graph")

        code = ""
        if data == "code":
            return code
        logger.debug(code)
        raise NotImplementedError("WIP.")

    def shared_view(self, url: Union[int, str], data: Literal["json", "code", "model", "svg", "png"] = "json"):
        """Takes a shared graph link and returns the data or the code to implement in python.

        Args:
            url: Id of the shared view (1453653298) or full/partial URL (`/diagrams/share/1453626097`)
            data: Defaults to return the data instead of printing the code

        Returns: The graph data or string representing the code to produce it.
        """
        url_id, _ = self.ipf._shared_url_id(url)
        return self._graph_url(url_id, data)


class IPFDiagram(Diagram):
    def __init__(self, ipf=None, **kwargs):
        warn(f"{self.__class__.__name__} will be removed in v6.9.", DeprecationWarning, stacklevel=2)
        logger.warning(f"{self.__class__.__name__} will be removed in v6.9.")
        if ipf:
            super().__init__(ipf)
        else:
            kwargs["timeout"] = kwargs.get("timeout", 15)
            super().__init__(IPFabricAPI(**kwargs))
