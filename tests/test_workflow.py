import unittest

from src.sample_data import SAMPLE_INTERNAL_BOM, SAMPLE_PRR, SAMPLE_VENDOR_QUOTES
from src.workflow import (
    AIAssistant,
    AgentKit,
    ChatKit,
    OpenAIWorkflow,
    as_internal_bom,
    as_requirements,
    as_vendor_quotes,
)


class WorkflowTests(unittest.TestCase):
    def test_buy_decision_returns_purchase_order(self) -> None:
        workflow = OpenAIWorkflow(
            agent_kit=AgentKit(),
            chat_kit=ChatKit(),
            assistant=AIAssistant(name="Test Assistant"),
        )
        requirement = as_requirements(SAMPLE_PRR)
        vendor_quotes = as_vendor_quotes(SAMPLE_VENDOR_QUOTES)
        internal_bom = as_internal_bom(SAMPLE_INTERNAL_BOM)

        result = workflow.run(requirement, vendor_quotes, internal_bom)

        self.assertEqual(result.decision.decision, "BUY")
        self.assertTrue(result.decision.rationale)
        self.assertEqual(result.artifact.status, "Order placed")


if __name__ == "__main__":
    unittest.main()
