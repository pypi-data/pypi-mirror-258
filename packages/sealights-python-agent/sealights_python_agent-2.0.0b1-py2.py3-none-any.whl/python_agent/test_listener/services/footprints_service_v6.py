import json
import logging
import time
import uuid
from typing import List

from python_agent.common.config_data import ConfigData
from python_agent.common.http.backend_proxy import BackendProxy

log = logging.getLogger(__name__)
AGENT_ID = str(uuid.uuid4())


class FootprintModel(object):
    def __init__(self, config_data: ConfigData):
        self.formatVersion = "6.0"
        self.meta = {
            "agentId": AGENT_ID,
            "labId": config_data.labId,
            "intervals": {
                "timedFootprintsCollectionIntervalSeconds": config_data.intervalSeconds
            }
        }
        self.methods = []
        self.executions = []
        self._hits = []
        self._last_start_time = self.get_current_time_milliseconds()
        self._total_lines = 0

    def has_hits(self):
        return bool(self._hits)

    def add_hits(self, methods: dict[str, List[int]], is_init_footprint: bool) -> 'FootprintModel':
        methods_indexes = []
        methods_lines: dict[str, List[int]] = {}
        for method, lines in methods.items():
            lines.sort()
            log.debug(f"Adding coverage method: {method} with lines: {lines}")
            self._total_lines += len(lines)
            if method not in self.methods:
                self.methods.append(method)
            method_index = self.methods.index(method)
            methods_indexes.append(method_index)
            methods_lines[str(method_index)] = lines
        end_time = self.get_current_time_milliseconds()
        self._last_start_time = end_time
        self._hits.append({
            "start": self._last_start_time,
            "end": end_time,
            "methods": methods_indexes,
            "methodLines": methods_lines,
            "isInitFootprints": is_init_footprint
        })
        return self

    def complete(self, execution_id: str) -> 'FootprintModel':
        self.executions.append(
            {
                "executionId": execution_id,
                "hits": self._hits
            }
        )
        log.debug(
            f"Footprints completed for lab id: {self.meta['labId']}, execution id: {execution_id}, methods: {len(self.methods)}, lines: {self._total_lines} in {len(self._hits)} hits")
        return self

    def to_json(self):
        return {
            "formatVersion": self.formatVersion,
            "meta": self.meta,
            "methods": self.methods,
            "executions": self.executions
        }

    def get_current_time_milliseconds(self):
        return int(round(time.time() * 1000))


#

class FootprintsService(object):
    def __init__(self, config_data: ConfigData, backend_proxy: BackendProxy):
        self.config_data = config_data
        self.backend_proxy = backend_proxy
        self.footprint_model = FootprintModel(config_data)

    def add_coverage(self, methods_coverage: dict[str, list[int]], is_init_footprint: bool):
        self.footprint_model.add_hits(methods_coverage, is_init_footprint)

    def has_coverage_recorded(self):
        return self.footprint_model.has_hits()

    def send(self, execution_id: str, test_stage: str, execution_build_session_id: str):
        if not self.footprint_model.has_hits():
            return
        self.footprint_model.complete(execution_id)
        data = json.dumps(self.footprint_model.to_json(), indent=4)
        self.backend_proxy.send_footprints_v6(data, execution_build_session_id, test_stage,
                                              self.config_data.buildSessionId)
        self.footprint_model = FootprintModel(self.config_data)
