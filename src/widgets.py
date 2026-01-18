from __future__ import annotations

WIDGETS = [
    {
        "id": "prr_form",
        "type": "form",
        "title": "Product Requirement Requisition",
        "fields": [
            {"key": "part_name", "label": "Part Name", "type": "text"},
            {"key": "quantity", "label": "Quantity", "type": "number"},
            {"key": "required_date", "label": "Required Date", "type": "date"},
            {"key": "specifications", "label": "Specifications", "type": "list"},
        ],
    },
    {
        "id": "decision_panel",
        "type": "summary",
        "title": "Make vs Buy Decision",
        "fields": [
            {"key": "decision", "label": "Decision"},
            {"key": "rationale", "label": "Rationale"},
        ],
    },
    {
        "id": "action_artifact",
        "type": "document",
        "title": "Generated Artifact",
        "fields": [
            {"key": "artifact_type", "label": "Artifact Type"},
            {"key": "artifact_id", "label": "Artifact ID"},
            {"key": "status", "label": "Status"},
        ],
    },
]
