import logging
from collections import defaultdict
from typing import Any, Union, List, Dict
from warnings import warn

from httpx import HTTPStatusError

from .intent_check import Group, IntentCheck

logger = logging.getLogger("ipfabric")
COLOR_DICT = dict(nan=-1, green=0, blue=10, amber=20, red=30)


def loaded_status(func):
    def _decorator(self, *args, **kwargs):
        if not self.loaded:
            logger.error("Intents are not loaded please run `ipf.intent.load_intent()`.")
        return func(self, *args, **kwargs)

    return _decorator


class Intent:
    def __init__(self, client, load=True):
        self.client: Any = client
        self.snapshot_id: str = self.client.snapshot_id
        self.loaded = self.snapshot_id and load
        self.intent_checks: List[IntentCheck] = self.get_intent_checks() if self.loaded else list()
        self.groups: List[Group] = self.get_groups() if self.loaded else list()

    def get_intent_checks(self, snapshot_id: str = None) -> List[IntentCheck]:
        """Gets all intent checks and returns a list of them.

        Args:
        snapshot_id: Optional snapshot ID to get different data

        Returns:
            list: List of intent checks
        """
        snapshot = self.client.snapshots[snapshot_id] if snapshot_id else self.client.snapshots[self.snapshot_id]
        if not snapshot.loaded:
            raise ValueError(f"Snapshot {snapshot.snapshot_id} is not loaded; cannot pull Intent Rules.")
        if snapshot.disabled_intent_verification is True:
            raise ValueError(
                f"Snapshot {snapshot.snapshot_id} has Intent Verification computation disabled; "
                "cannot pull Intent Rules."
            )
        res = self.client.get("reports", params=dict(snapshot=snapshot.snapshot_id))
        try:
            res.raise_for_status()
            return [IntentCheck(**check) for check in res.json()]
        except HTTPStatusError:
            logger.warning(self.client._api_insuf_rights + 'on GET "/reports". Will not load Intents.')
            return list()

    def load_intent(self, snapshot_id: str = None):
        """Loads intent checks into the class.

        Args:
            snapshot_id: Uses a different Snapshot ID then client
        """
        self.snapshot_id = snapshot_id or self.client.snapshot_id
        self.intent_checks = self.get_intent_checks(snapshot_id)
        self.groups = self.get_groups()
        self.loaded = True

    def get_groups(self) -> list:
        """

        Returns:
            list: list of groups
        """
        res = self.client.get("reports/groups")
        try:
            res.raise_for_status()
            return [Group(**group) for group in res.json()]
        except HTTPStatusError:
            logger.warning(self.client._api_insuf_rights + 'on GET "/reports/groups". Will not load Intent Groups.')
            return list()

    @property
    @loaded_status
    def custom(self) -> List[IntentCheck]:
        return [c for c in self.intent_checks if c.custom]

    @property
    @loaded_status
    def builtin(self) -> List[IntentCheck]:
        return [c for c in self.intent_checks if not c.custom]

    @property
    @loaded_status
    def intent_by_id(self) -> Dict[str, IntentCheck]:
        return {c.intent_id: c for c in self.intent_checks}

    @property
    @loaded_status
    def intents_by_name(self) -> Dict[str, List[IntentCheck]]:
        reports = defaultdict(list)
        [reports[c.name].append(c) for c in self.intent_checks]
        return dict(reports)

    @property
    @loaded_status
    def intent_by_name(self) -> Dict[str, IntentCheck]:
        msg = (
            "This method will be removed in v6.10/v7.0. "
            "Please use IPFClient().intent.intents_by_name() as Intent Names are not unique."
        )
        warn(
            msg,
            DeprecationWarning,
            stacklevel=2,
        )
        logger.warning(msg)
        return {c.name: c for c in self.intent_checks}

    @property
    @loaded_status
    def intent_ids_by_web_endpoint(self) -> Dict[str, List[str]]:
        reports = defaultdict(list)
        [reports[c.web_endpoint].append(c.intent_id) for c in self.intent_checks]
        return dict(reports)

    @property
    @loaded_status
    def intent_ids_by_api_endpoint(self) -> Dict[str, List[str]]:
        reports = defaultdict(list)
        [reports[c.api_endpoint].append(c.intent_id) for c in self.intent_checks]
        return dict(reports)

    @property
    @loaded_status
    def group_by_id(self) -> Dict[str, Group]:
        return {g.group_id: g for g in self.groups}

    @property
    @loaded_status
    def group_by_name(self) -> Dict[str, Group]:
        return {g.name: g for g in self.groups}

    @loaded_status
    def get_results(self, intent: IntentCheck, color: Union[str, int], snapshot_id: str = None) -> list:
        """Get the outcome of an Intent Check by a specific color

        Args:
            intent: an IntentCheck, please see the Intent Check Model
            color: color of intent check
            snapshot_id: Uses a different Snapshot ID then client

        Returns:
            list: List of Dictionary objects.
        """
        if isinstance(color, str):
            color = COLOR_DICT[color]
        return self._get_data(intent, snapshot_id or self.snapshot_id, color)

    @loaded_status
    def get_all_results(self, intent: IntentCheck, snapshot_id: str = None):
        """set the intent check attributes

        Args:
            intent: an IntentCheck, please see the Intent Check Model
            snapshot_id: Uses a different Snapshot ID then client

        Returns:
            list: List of Dictionary objects.
        """
        snapshot_id = snapshot_id or self.snapshot_id
        for color_str, color_int in COLOR_DICT.items():
            if color_int == -1 or getattr(intent.result.checks, color_str):
                setattr(intent.result_data, color_str, self._get_data(intent, snapshot_id, color_int))
        return intent

    def _get_data(self, intent: IntentCheck, snapshot_id: str, color: int):
        return self.client.fetch_all(
            intent.api_endpoint,
            snapshot_id=snapshot_id,
            reports=intent.web_endpoint,
            filters={intent.column: ["color", "eq", color]},
        )

    @loaded_status
    def compare_snapshot(self, snapshot_id: str, reverse: bool = False) -> list:
        """Compares all intents against another snapshot.
        Current is the snapshot loaded into the class
        Other is the snapshot specified in this method.  Use reverse=True to flip them.

        Args:
            snapshot_id: Snapshot ID to compare against this will be the "other" key
            reverse: Default False, setting to true will flip current and other.
        Returns:
            list: List of dictionaries
        """
        # TODO: Fix
        new_intents = {i.name: i for i in self.get_intent_checks(snapshot_id)}
        comparison = list()
        for name, intent in new_intents.items():
            old = self.intents_by_name[name][0].result
            compare = intent.result.compare(old) if reverse else old.compare(intent.result)
            for desc, value in compare.items():
                n = desc if desc != "count" else "total"
                comparison.append({"name": name, "id": intent.intent_id, "check": n, **value})
        return comparison
