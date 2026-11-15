
# Mock tools: no external APIs or credentials required.

def search_policy(question: str) -> str:
    """Simulates retrieval from a policy knowledge base."""
    if "baggage" in question.lower():
        return (
            "Baggage claims require a case number "
            "and supporting documents."
        )

    return ""


def fetch_booking(question: str) -> str:
    """Simulates an external booking API."""
    if "timeout" in question.lower():
        raise TimeoutError("booking API timeout")

    return "Booking status: CONFIRMED"
