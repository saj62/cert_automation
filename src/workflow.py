from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class PartsDetails:
    part_number: str
    description: str
    quantity: int
    required_date: str
    specs: List[str]


@dataclass
class Decision:
    decision: str
    rationale: List[str]
    selected_vendor: str | None = None


@dataclass
class PurchaseOrder:
    po_id: str
    vendor: str
    part_number: str
    quantity: int
    unit_cost: float
    status: str


@dataclass
class WorkOrder:
    wo_id: str
    part_number: str
    quantity: int
    status: str


@dataclass
class WorkflowResult:
    parts_details: PartsDetails
    decision: Decision
    artifact: PurchaseOrder | WorkOrder


@dataclass
class BusinessRules:
    budget_cap_per_unit: float
    max_lead_time_days: int
    preferred_vendors: List[str]
    production_capacity_units_per_week: int


@dataclass
class VendorQuote:
    vendor: str
    unit_cost: float
    lead_time_days: int
    moq: int
    part_number: str


@dataclass
class InternalBOM:
    part_number: str
    build_cost: float
    build_lead_time_days: int
    risk_notes: str


@dataclass
class ProductRequirement:
    prr_id: str
    requestor: str
    part_name: str
    quantity: int
    required_date: str
    specifications: List[str]
    constraints: BusinessRules


@dataclass
class AgentKit:
    """Mock Agent Kit representing task routing and orchestration."""

    def route(self, intent: str) -> str:
        return f"Routed to agent: {intent}"


@dataclass
class ChatKit:
    """Mock Chat Kit representing conversational UX components."""

    def prompt(self, message: str) -> str:
        return f"Assistant prompt: {message}"


@dataclass
class AIAssistant:
    name: str

    def summarize(self, text: str) -> str:
        return f"{self.name} summary: {text}"


@dataclass
class OpenAIWorkflow:
    agent_kit: AgentKit
    chat_kit: ChatKit
    assistant: AIAssistant

    def run(
        self,
        requirement: ProductRequirement,
        vendor_quotes: List[VendorQuote],
        internal_bom: InternalBOM,
    ) -> WorkflowResult:
        parts_details = PartsDetails(
            part_number=internal_bom.part_number,
            description=requirement.part_name,
            quantity=requirement.quantity,
            required_date=requirement.required_date,
            specs=requirement.specifications,
        )

        decision, rationale, selected_vendor = self._make_buy_decision(
            requirement,
            vendor_quotes,
            internal_bom,
        )

        if decision == "BUY" and selected_vendor:
            best_quote = next(
                quote for quote in vendor_quotes if quote.vendor == selected_vendor
            )
            artifact = PurchaseOrder(
                po_id=f"PO-{requirement.prr_id}",
                vendor=best_quote.vendor,
                part_number=best_quote.part_number,
                quantity=requirement.quantity,
                unit_cost=best_quote.unit_cost,
                status="Order placed",
            )
        else:
            artifact = WorkOrder(
                wo_id=f"WO-{requirement.prr_id}",
                part_number=internal_bom.part_number,
                quantity=requirement.quantity,
                status="Released to production",
            )

        return WorkflowResult(
            parts_details=parts_details,
            decision=Decision(
                decision=decision,
                rationale=rationale,
                selected_vendor=selected_vendor,
            ),
            artifact=artifact,
        )

    def _make_buy_decision(
        self,
        requirement: ProductRequirement,
        vendor_quotes: List[VendorQuote],
        internal_bom: InternalBOM,
    ) -> Tuple[str, List[str], str | None]:
        rationale: List[str] = []
        sorted_quotes = sorted(vendor_quotes, key=lambda quote: quote.unit_cost)
        best_quote = sorted_quotes[0]

        meets_budget = best_quote.unit_cost <= requirement.constraints.budget_cap_per_unit
        meets_lead_time = (
            best_quote.lead_time_days <= requirement.constraints.max_lead_time_days
        )
        capacity_needed_weeks = requirement.quantity / requirement.constraints.production_capacity_units_per_week
        internal_time = max(internal_bom.build_lead_time_days, int(capacity_needed_weeks * 7))

        if meets_budget:
            rationale.append(
                f"Vendor cost {best_quote.unit_cost} within budget cap {requirement.constraints.budget_cap_per_unit}."
            )
        else:
            rationale.append(
                f"Vendor cost {best_quote.unit_cost} exceeds budget cap {requirement.constraints.budget_cap_per_unit}."
            )

        if meets_lead_time:
            rationale.append(
                f"Vendor lead time {best_quote.lead_time_days} days meets requirement {requirement.constraints.max_lead_time_days} days."
            )
        else:
            rationale.append(
                f"Vendor lead time {best_quote.lead_time_days} days exceeds requirement {requirement.constraints.max_lead_time_days} days."
            )

        rationale.append(
            f"Internal build cost {internal_bom.build_cost} with lead time {internal_time} days."
        )

        if meets_budget and meets_lead_time:
            return "BUY", rationale, best_quote.vendor

        return "MAKE", rationale, None


def as_requirements(payload: Dict[str, object]) -> ProductRequirement:
    constraints = payload["constraints"]
    rules = BusinessRules(
        budget_cap_per_unit=constraints["budget_cap_per_unit"],
        max_lead_time_days=constraints["max_lead_time_days"],
        preferred_vendors=constraints["preferred_vendors"],
        production_capacity_units_per_week=constraints["production_capacity_units_per_week"],
    )
    return ProductRequirement(
        prr_id=payload["prr_id"],
        requestor=payload["requestor"],
        part_name=payload["part_name"],
        quantity=payload["quantity"],
        required_date=payload["required_date"],
        specifications=payload["specifications"],
        constraints=rules,
    )


def as_vendor_quotes(payload: List[Dict[str, object]]) -> List[VendorQuote]:
    return [
        VendorQuote(
            vendor=item["vendor"],
            unit_cost=item["unit_cost"],
            lead_time_days=item["lead_time_days"],
            moq=item["moq"],
            part_number=item["part_number"],
        )
        for item in payload
    ]


def as_internal_bom(payload: Dict[str, object]) -> InternalBOM:
    return InternalBOM(
        part_number=payload["part_number"],
        build_cost=payload["build_cost"],
        build_lead_time_days=payload["build_lead_time_days"],
        risk_notes=payload["risk_notes"],
    )
