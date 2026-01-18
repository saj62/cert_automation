from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MCPResource:
    name: str
    payload: Dict[str, str]


class MCPServer:
    """Minimal in-memory MCP server mock used for demo workflows."""

    def __init__(self) -> None:
        self._resources: List[MCPResource] = []

    def publish(self, name: str, payload: Dict[str, str]) -> MCPResource:
        resource = MCPResource(name=name, payload=payload)
        self._resources.append(resource)
        return resource

    def list_resources(self) -> List[MCPResource]:
        return list(self._resources)
