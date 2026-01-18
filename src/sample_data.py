from __future__ import annotations

SAMPLE_PRR = {
    "prr_id": "PRR-2025-0007",
    "requestor": "Graduate AI Lab",
    "part_name": "Adaptive Sensor Module",
    "quantity": 250,
    "required_date": "2025-03-15",
    "specifications": [
        "ISO 9001 compliance",
        "IP67 enclosure",
        "Temperature range -20C to 85C",
    ],
    "constraints": {
        "budget_cap_per_unit": 120.0,
        "max_lead_time_days": 21,
        "preferred_vendors": ["Nova Components", "Atlas Supply"],
        "production_capacity_units_per_week": 120,
    },
}

SAMPLE_VENDOR_QUOTES = [
    {
        "vendor": "Nova Components",
        "unit_cost": 98.0,
        "lead_time_days": 14,
        "moq": 100,
        "part_number": "NC-ASM-442",
    },
    {
        "vendor": "Atlas Supply",
        "unit_cost": 105.0,
        "lead_time_days": 18,
        "moq": 50,
        "part_number": "AS-0199",
    },
]

SAMPLE_INTERNAL_BOM = {
    "part_number": "INT-ASM-110",
    "build_cost": 112.0,
    "build_lead_time_days": 28,
    "risk_notes": "Requires calibration rig downtime during week 2.",
}
