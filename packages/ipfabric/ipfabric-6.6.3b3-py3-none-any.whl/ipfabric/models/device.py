from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ipfabric.client import EXPORT_FORMAT

try:
    from pandas import DataFrame
except ImportError:
    DataFrame = None

import re
import logging
from datetime import timedelta
from ipfabric.settings import Attributes
from httpx import HTTPStatusError
from typing import Optional, List, Union, Dict, DefaultDict, Set, overload, Literal, Any
from ipaddress import IPv4Interface
from collections import defaultdict
from case_insensitive_dict import CaseInsensitiveDict
from ipfabric.models.technology import Technology
from ipfabric.tools.shared import create_filter

from pydantic import BaseModel, Field, PrivateAttr
from ipfabric.exceptions import deprecated_args_decorator

logger = logging.getLogger("ipfabric")


class DeviceConfig(BaseModel):
    status: str
    current: Optional[str] = Field(None, alias="currentConfig")
    start: Optional[str] = Field(None, alias="startupConfig")


class Device(BaseModel):
    client: Optional[Any] = None
    attributes: Optional[dict] = None
    global_attributes: Optional[dict] = None
    domain: Optional[str] = None
    family: Optional[str] = None
    fqdn: Optional[str] = None
    hostname: str
    image: Optional[str] = None
    model: Optional[str] = None
    platform: Optional[str] = None
    processor: Optional[str] = None
    reload: Optional[str] = None
    sn: str
    uptime: Optional[timedelta] = None
    vendor: str
    version: Optional[str] = None
    blob_key: Optional[str] = Field(None, alias="blobKey")
    config_reg: Optional[str] = Field(None, alias="configReg")
    dev_type: str = Field(None, alias="devType")
    hostname_original: Optional[str] = Field(None, alias="hostnameOriginal")
    hostname_processed: Optional[str] = Field(None, alias="hostnameProcessed")
    login_ip: Optional[IPv4Interface] = Field(None, alias="loginIp")
    login_type: str = Field(None, alias="loginType")
    mem_total_bytes: Optional[float] = Field(None, alias="memoryTotalBytes")
    mem_used_bytes: Optional[float] = Field(None, alias="memoryUsedBytes")
    mem_utilization: Optional[float] = Field(None, alias="memoryUtilization")
    object_id: Optional[str] = Field(None, alias="objectId")
    routing_domain: Optional[int] = Field(None, alias="rd")
    site_name: str = Field(None, alias="siteName")
    sn_hw: str = Field(None, alias="snHw")
    stp_domain: Optional[int] = Field(None, alias="stpDomain")
    task_key: Optional[str] = Field(None, alias="taskKey")
    slug: Optional[str] = None

    def __repr__(self):
        return self.hostname

    def __str__(self):
        return self.hostname

    def __eq__(self, other):
        return self.sn == other.sn if isinstance(other, Device) else str(other)

    def __hash__(self):
        return hash(self.sn)

    @property
    def technology(self):
        return Technology(client=self.client, sn=self.sn)

    @property
    def site(self):
        return self.site_name

    @property
    def local_attributes(self):
        return self.attributes

    @classmethod
    def check_attribute(cls, attribute) -> True:
        if attribute not in cls.model_fields:
            raise AttributeError(f"Attribute {attribute} not in Device class.")
        return True

    @deprecated_args_decorator(version="6.8.0")
    def get_log_file(self, **kwargs) -> str:
        res = self.client.get("/os/logs/task/" + self.task_key)
        res.raise_for_status()
        return res.text

    @deprecated_args_decorator(version="6.8.0")
    def get_config(self, **kwargs) -> Union[None, DeviceConfig]:
        if not self.blob_key:
            logger.warning("Device Config not in Snapshot File. Please try using ipfabric.tools.DeviceConfigs")
            return None
        res = self.client.get("blobs/device-configuration/" + str(self.blob_key))
        res.raise_for_status()
        return DeviceConfig(**res.json())

    @deprecated_args_decorator(version="6.8.0")
    def interfaces(self, **kwargs) -> list:
        return self.client.inventory.interfaces.all(filters={"sn": ["eq", self.sn]})

    @deprecated_args_decorator(version="6.8.0")
    def pn(self, **kwargs) -> list:
        return self.client.inventory.pn.all(filters={"deviceSn": ["eq", self.sn]})

    @deprecated_args_decorator(version="6.8.0")
    def switchport(self, **kwargs) -> list:
        return self.technology.interfaces.switchport.all()

    @deprecated_args_decorator(version="6.8.0")
    def managed_ip_ipv4(self, **kwargs) -> list:
        return self.technology.addressing.managed_ip_ipv4.all()

    @deprecated_args_decorator(version="6.8.0")
    def managed_ip_ipv6(self, **kwargs) -> list:
        return self.technology.addressing.managed_ip_ipv6.all()

    @deprecated_args_decorator(version="6.8.0")
    def mac_table(self, **kwargs) -> list:
        return self.technology.addressing.mac_table.all()

    @deprecated_args_decorator(version="6.8.0")
    def arp_table(self, **kwargs) -> list:
        return self.technology.addressing.arp_table.all()

    @deprecated_args_decorator(version="6.8.0")
    def routes_ipv4(self, **kwargs) -> list:
        return self.technology.routing.routes_ipv4.all()

    @deprecated_args_decorator(version="6.8.0")
    def routes_ipv6(self, **kwargs) -> list:
        return self.technology.routing.routes_ipv6.all()

    @deprecated_args_decorator(version="6.8.0")
    def neighbors_all(self, **kwargs) -> list:
        return self.technology.neighbors.neighbors_all.all()

    def trigger_backup(self):
        return self.client.trigger_backup(sn=self.sn)

    @overload
    def fetch_all(
        self,
        client: Any,
        url: str,
        export: Literal["csv"],
        columns: List[str] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
    ) -> List[dict]: ...

    @overload
    def fetch_all(
        self,
        client: Any,
        url: str,
        export: Literal["csv"],
        columns: List[str] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        csv_tz: Optional[str] = None,
    ) -> bytes: ...

    @overload
    def fetch_all(
        self,
        client: Any,
        url: str,
        export: Literal["df"],
        columns: List[str] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
    ) -> DataFrame: ...

    @deprecated_args_decorator(version="6.8.0", arg_type="IPFClient", no_args=False)
    def fetch_all(
        self,
        client: Any,
        url: str,
        export: EXPORT_FORMAT = "json",
        columns: List[str] = None,
        filters: Optional[Union[dict, str]] = None,
        snapshot_id: Optional[str] = None,
        reports: Optional[Union[bool, list, str]] = False,
        sort: Optional[dict] = None,
        csv_tz: Optional[str] = None,
    ):
        """Gets all data from IP Fabric for specified endpoint filtered on the `sn` of the device

        Args:
            url: Example tables/vlan/device-summary
            export: str: Export format to return [json, csv]; default is json.
            columns: Optional list of columns to return, None will return all
            filters: Optional dictionary of filters which will be merged with the sn filter
            snapshot_id: Optional snapshot_id to override default
            reports: String of frontend URL where the reports are displayed or a list of report IDs
            sort: Optional dictionary to apply sorting: {"order": "desc", "column": "lastChange"}
            csv_tz: str: Default None, set a timezone to return human-readable dates when using CSV;
                         see `ipfabric.tools.shared.TIMEZONES`
        Returns:
            Union[List[dict], bytes, pandas.DataFrame]: List of dict if json, bytes string if CSV, DataFrame is df
        """
        all_columns, f = create_filter(self.client, url, filters, self.sn)
        return self.client.fetch_all(
            url,
            filters=f,
            columns=columns or all_columns,
            export=export,
            snapshot_id=snapshot_id,
            reports=reports,
            sort=sort,
            csv_tz=csv_tz,
        )


class DeviceDict(CaseInsensitiveDict):
    """CaseInsensitiveDict with functions to search or regex on dictionary keys."""

    def __init__(self, attribute, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attribute = attribute

    @staticmethod
    def _new_dict(a):
        return DeviceDict[str, Device](attribute=a) if a == "sn" else DeviceDict[str, List[Device]](attribute=a)

    @overload
    def regex(self: DeviceDict[str, List[Device]], pattern: str, *flags: int) -> DeviceDict[str, List[Device]]: ...

    @overload
    def regex(self: DeviceDict[str, Device], pattern: str, *flags: int) -> DeviceDict[str, Device]: ...

    def regex(self, pattern: str, *flags: int) -> DeviceDict[str, Union[List[Device], Device]]:
        """
        Case-sensitive regex search on dictionary keys.
        Args:
            pattern: str: Regex string to search.
            *flags: int or re.RegexFlag: Regex flags to use.

        Returns:
            DeviceDict: New instance of DeviceDict (CaseInsensitiveDict)
        """
        regex = re.compile(pattern, flags=sum(flags))
        new_dict = self._new_dict(self.attribute)
        [new_dict.update({key: value}) for key, value in self._data.values() if key and regex.search(key)]
        return new_dict

    @overload
    def search(
        self: DeviceDict[str, List[Device]], pattern: Union[List[str], str]
    ) -> DeviceDict[str, List[Device]]: ...

    @overload
    def search(self: DeviceDict[str, Device], pattern: Union[List[str], str]) -> DeviceDict[str, Device]: ...

    def search(self, pattern: Union[List[str], str]) -> DeviceDict[str, Union[List[Device], Device]]:
        """
        Case-insensitive search on dictionary keys.
        Args:
            pattern: Union[List[str], str]: String or List of strings to match on.

        Returns:
            DeviceDict: New instance of DeviceDict (CaseInsensitiveDict)
        """
        pattern = [pattern.lower()] if isinstance(pattern, str) else [p.lower() for p in pattern]
        new_dict = self._new_dict(self.attribute)
        [new_dict.update({o_key: value}) for key, (o_key, value) in self._data.items() if key in pattern]
        return new_dict

    def _flatten_devs(self) -> List[Device]:
        devices = list()
        for value in self.values():
            if isinstance(value, list):
                devices.extend(value)
            else:
                devices.append(value)
        return devices

    def sub_search(self, attribute: str, pattern: Union[List[str], str]) -> DeviceDict[str, List[Device]]:
        """
        Case-insensitive sub search of another Device attribute.
        Args:
            attribute: str: Attribute of Device class.
            pattern: Union[List[str], str]: String or List of strings to match on.

        Returns:
             DeviceDict: New instance of DeviceDict (CaseInsensitiveDict) grouped by new attribute.
        """
        Device.check_attribute(attribute)
        return Devices.group_dev_by_attr(self._flatten_devs(), attribute).search(pattern)

    def sub_regex(self, attribute: str, pattern: Union[List[str], str], *flags: int) -> DeviceDict[str, List[Device]]:
        """
        Case-sensitive regex sub search of another Device attribute.
        Args:
            attribute: str: Attribute of Device class.
            pattern: str: Regex string to search.
            *flags: int or re.RegexFlag: Regex flags to use.

        Returns:
            DeviceDict: New instance of DeviceDict (CaseInsensitiveDict) grouped by new attribute.
        """
        Device.check_attribute(attribute)
        return Devices.group_dev_by_attr(self._flatten_devs(), attribute).regex(pattern, *flags)


class Devices(BaseModel):
    snapshot_id: str
    client: Any
    _attrs: Optional[DefaultDict[str, Set[str]]] = PrivateAttr()
    _global_attrs: Optional[DefaultDict[str, Set[str]]] = PrivateAttr()
    _all: List[Device] = PrivateAttr()

    def __init__(
        self,
        snapshot_id: str,
        client: Any,
        devices: Optional[List[dict]] = None,
        device_filters: Optional[dict] = None,
        device_attr_filters: Optional[dict] = None,
    ):
        super().__init__(snapshot_id=snapshot_id, client=client)
        self.update(devices, device_filters, device_attr_filters)

    def update(self, devices: List[dict] = None, device_filters: dict = None, device_attr_filters: dict = None):
        devices = devices if devices else self._load_devices(device_filters, device_attr_filters)
        if not devices:
            return None
        try:
            self._attrs, lcl_attr = self._parse_attrs(
                Attributes(client=self.client, snapshot_id=self.client.snapshot_id).all()
            )
        except HTTPStatusError:
            logger.warning(
                self.client._api_insuf_rights
                + 'on POST "/tables/snapshot-attributes". Cannot load Local (snapshot) Attributes in Devices.'
            )
            lcl_attr = dict()
        try:
            self._global_attrs, glb_attr = self._parse_attrs(Attributes(client=self.client).all())
        except HTTPStatusError:
            logger.warning(
                self.client._api_insuf_rights
                + 'on POST "/tables/global-attributes". Cannot load Global Attributes in Devices.'
            )
            glb_attr = dict()
        try:
            blob_keys = {
                b["sn"]: b["blobKey"]
                for b in self.client.fetch_all("/tables/management/configuration/saved", columns=["sn", "blobKey"])
            }
        except HTTPStatusError:
            logger.warning(
                self.client._api_insuf_rights + 'on POST "/tables/management/configuration/saved". '
                "You will not be able to pull device config from Device model."
            )
            blob_keys = dict()
        self._all = [
            Device(
                **d,
                attributes=lcl_attr.get(d["sn"], dict()),
                global_attributes=glb_attr.get(d["sn"], dict()),
                blobKey=blob_keys.get(d["sn"], None),
                client=self.client,
            )
            for d in devices
        ]

    def _load_devices(self, device_filters: dict = None, device_attr_filters: dict = None):
        if self.client._no_loaded_snapshots:
            logger.warning("No loaded snapshots, cannot load devices.")
        else:
            if not device_attr_filters and self.client.attribute_filters:
                logger.warning(
                    f"Global `attribute_filters` is set; only pulling devices matching:\n{self.client.attribute_filters}."
                )
            try:
                return self.client.inventory.devices.all(filters=device_filters, attr_filters=device_attr_filters)
            except HTTPStatusError:
                logger.warning(self._api_insuf_rights + 'on POST "/tables/inventory/devices". Will not load Devices.')
        return list()

    @staticmethod
    def _parse_attrs(attributes: List[dict] = None):
        if not attributes:
            return None, dict()
        cls_attr, dev_attr = defaultdict(set), defaultdict(dict)
        for d in attributes:
            dev_attr[d["sn"]].update({d["name"]: d["value"]})
            cls_attr[d["name"]].add(d["value"])
        return cls_attr, dev_attr

    @property
    def all(self) -> List[Device]:
        """Returns List[Device]."""
        return self._all

    def _check_attr_name(self, name: str) -> bool:
        if self._attrs is None:
            logger.warning("Attributes were not loaded into devices.")
        elif name not in self._attrs:
            logger.warning(f'Attribute key "{name}" not found in snapshot "{self.snapshot_id}".')
        else:
            return True
        return False

    def _filter_attr(self, devs: Set[Device], name: str, values: Union[List[str], str]) -> Set[Device]:
        if not self._check_attr_name(name):
            return set()
        values = values if isinstance(values, list) else [values]
        for dev in devs.copy():
            dev_attr = dev.attributes.get(name, None)
            if not dev_attr or dev_attr not in values:
                devs.discard(dev)
        return devs

    def filter_by_attr(self, name: str, values: Union[List[str], str]) -> List[Device]:
        """
        Return list of devices with an attribute set to a value
        Args:
            name: str: Attribute name
            values: Union[List[str], str]: Single attribute value or list of values to match.
        Returns:
            List[Device]
        """
        return list(self._filter_attr(set(self.all.copy()), name, values))

    def filter_by_attrs(self, attr_filter: Dict[str, Union[List[str], str]]) -> List[Device]:
        """
        Return list of devices matching multiple key/value attribute pairs
        Args:
            attr_filter: dict: {'ATTR_1': 'VALUE_1', 'ATTR_2': ['VALUE_2', 'VALUE_3']}
        Returns:
            List[Device]
        """
        devs = set(self.all.copy())
        for k, v in attr_filter.items():
            devs = self._filter_attr(devs, k, v)
        return list(devs)

    def has_attr(self, name: str) -> List[Device]:
        """
        Return list of devices that has an attribute set matching name.
        Args:
            name: str: Attribute name
        Returns:
            List[Device]
        """
        return [d for d in self.all if d.attributes.get(name, None)] if self._check_attr_name(name) else list()

    def does_not_have_attr(self, name: str) -> List[Device]:
        """
        Return list of devices that does not have an attribute set matching name.
        Args:
            name: str: Attribute name
        Returns:
            List[Device]
        """
        return [d for d in self.all if not d.attributes.get(name, None)] if self._check_attr_name(name) else list()

    def _group_dev_by_attr(self, attribute: str) -> DeviceDict[str, List[Device]]:
        return self.group_dev_by_attr(self._all, attribute)

    @classmethod
    def group_dev_by_attr(cls, devices: List[Device], attribute: str) -> DeviceDict[str, List[Device]]:
        devs = defaultdict(list)
        [devs[getattr(d, attribute)].append(d) for d in devices]
        return DeviceDict(attribute=attribute, data=devs)

    @property
    def by_sn(self) -> DeviceDict[str, Device]:
        """Returns Case-insensitive DeviceDict {'sn': Device}."""
        return DeviceDict(attribute="sn", data={d.sn: d for d in self._all})

    @property
    def by_hostname_original(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'hostname': [Device]}."""
        return self._group_dev_by_attr("hostname_original")

    @property
    def by_hostname(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'hostname': [Device]}."""
        return self._group_dev_by_attr("hostname")

    @property
    def by_sn_hw(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'sn_hw': [Device]}."""
        return self._group_dev_by_attr("sn_hw")

    @property
    def by_site(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'site': [Device]}."""
        return self._group_dev_by_attr("site")

    @property
    def by_vendor(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'vendor': [Device]}."""
        return self._group_dev_by_attr("vendor")

    @property
    def by_family(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'family': [Device]}."""
        return self._group_dev_by_attr("family")

    @property
    def by_platform(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'platform': [Device]}."""
        return self._group_dev_by_attr("platform")

    @property
    def by_model(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'model': [Device]}."""
        return self._group_dev_by_attr("model")

    @property
    def by_version(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'version': [Device]}."""
        return self._group_dev_by_attr("version")

    @property
    def by_fqdn(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'version': [Device]}."""
        return self._group_dev_by_attr("fqdn")

    @property
    def by_login_type(self) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'version': [Device]}."""
        return self._group_dev_by_attr("login_type")

    def by_custom(self, attribute) -> DeviceDict[str, List[Device]]:
        """Returns Case-insensitive DeviceDict {'version': [Device]}."""
        Device.check_attribute(attribute)
        return self._group_dev_by_attr(attribute)
