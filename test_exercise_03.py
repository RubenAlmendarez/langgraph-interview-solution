
import unittest
from exercise_03 import build_graph


class TestLangGraphWorkflow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = build_graph()

    def run_case(self, question):
        return self.app.invoke({
            "question": question,
            "route": "",
            "context": "",
            "error": "",
            "answer": ""
        })

    def test_policy_retrieval(self):
        result = self.run_case("What is the baggage policy?")
        self.assertEqual(result["route"], "policy")
        self.assertIn("Baggage claims", result["answer"])

    def test_booking_tool(self):
        result = self.run_case("Check my booking")
        self.assertEqual(result["route"], "booking")
        self.assertIn("CONFIRMED", result["answer"])

    def test_api_failure(self):
        result = self.run_case("Booking timeout")
        self.assertIn("ESCALATED", result["answer"])
        self.assertIn("timeout", result["error"])

    def test_unknown_request(self):
        result = self.run_case("Tell me a joke")
        self.assertEqual(result["route"], "fallback")
        self.assertIn("ESCALATED", result["answer"])

    def test_missing_policy(self):
        result = self.run_case("What is the refund policy?")
        self.assertEqual(result["route"], "policy")
        self.assertIn("No matching policy", result["answer"])


if __name__ == "__main__":
    unittest.main()
