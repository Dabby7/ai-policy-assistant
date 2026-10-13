
from decimal import Decimal

from src.assistant import ask
from src.calculator import calculate_upi_fee


def test_large_merchant_fee():
    fee = calculate_upi_fee(4000, 1000001, "2026-08-15")
    assert fee["mdr"] == Decimal("20.00")
    assert fee["gst"] == Decimal("3.60")
    assert fee["total_fee"] == Decimal("23.60")


def test_large_merchant_cap():
    fee = calculate_upi_fee(150000, 1000001, "2026-08-15")
    assert fee["mdr"] == Decimal("25.00")
    assert fee["gst"] == Decimal("4.50")
    assert fee["total_fee"] == Decimal("29.50")


def test_refund_before_september():
    result = ask(
        "Does the merchant get MDR back for a refund within 3 hours?",
        "2026-08-20",
    )
    assert "reversed in full" in result["answer"]
    assert result["status"] == "CONFLICT_RESOLVED"


def test_refund_after_september():
    result = ask(
        "Does the merchant get MDR back for a refund within 3 hours?",
        "2026-09-05",
    )
    assert "not returned" in result["answer"]
    assert result["status"] == "CONFLICT_RESOLVED"


def test_unknown_question():
    result = ask("What is the merchant's favourite colour?")
    assert result["status"] == "CANNOT_ANSWER"
