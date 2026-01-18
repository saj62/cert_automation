from __future__ import annotations

import json
from dataclasses import asdict
from typing import Dict

from mcp_server import MCPServer
from sample_data import SAMPLE_INTERNAL_BOM, SAMPLE_PRR, SAMPLE_VENDOR_QUOTES
from widgets import WIDGETS
from workflow import (
    AIAssistant,
    AgentKit,
    ChatKit,
    OpenAIWorkflow,
    as_internal_bom,
    as_requirements,
    as_vendor_quotes,
)


def build_openai_agent_spec() -> Dict[str, object]:
    """Represent an OpenAI Agent Builder spec for the workflow."""
    return {
        "agent_name": "MakeBuyDecisionAgent",
        "description": "Collects PRR data, decides make vs buy, and triggers the correct order type.",
        "model": "gpt-4.1",
        "instructions": [
            "Validate required fields in PRR.",
            "Summarize parts details.",
            "Apply business rules to decide make vs buy.",
            "Generate a PO or Work Order based on the decision.",
        ],
        "tools": [
            "parts_catalog.lookup",
            "vendor_quotes.list",
            "production.schedule",
            "orders.create_purchase_order",
            "orders.create_work_order",
        ],
        "widgets": WIDGETS,
    }


def run_demo() -> Dict[str, object]:
    agent_kit = AgentKit()
    chat_kit = ChatKit()
    assistant = AIAssistant(name="Sourcing Copilot")
    workflow = OpenAIWorkflow(agent_kit=agent_kit, chat_kit=chat_kit, assistant=assistant)

    requirement = as_requirements(SAMPLE_PRR)
    vendor_quotes = as_vendor_quotes(SAMPLE_VENDOR_QUOTES)
    internal_bom = as_internal_bom(SAMPLE_INTERNAL_BOM)

    mcp_server = MCPServer()
    mcp_server.publish("prr", {"id": requirement.prr_id, "requestor": requirement.requestor})

    result = workflow.run(requirement, vendor_quotes, internal_bom)

    output = {
        "agent_builder_spec": build_openai_agent_spec(),
        "mcp_resources": [asdict(resource) for resource in mcp_server.list_resources()],
        "workflow_result": {
            "parts_details": asdict(result.parts_details),
            "decision": asdict(result.decision),
            "artifact": asdict(result.artifact),
        },
        "assistant_summary": assistant.summarize(
            f"Decision {result.decision.decision} for PRR {requirement.prr_id}."
        ),
    }
    return output


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2))
