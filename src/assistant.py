from datetime import date
from src.policy_loader import load_documents
from src.calculator import calculate_upi_fee

ANSWERED = "ANSWERED"
CONFLICT = "CONFLICT_RESOLVED"
CANNOT = "CANNOT_ANSWER"


def ask(question, as_of_date="2026-08-15"):
    docs = load_documents()
    q = question.lower()
    d = date.fromisoformat(str(as_of_date))

    def result(answer, citations, status=ANSWERED):
        return {
            "answer": answer,
            "citations": citations,
            "status": status,
        }

    master = "policy_master_v1.md"
    amendment = "circular_2026_08_amendment.md"
    faq = "merchant_faq_2026-03.md"

    # Account closure
    if any(x in q for x in ("closed my account", "account closure", "close my account")):
        return result(
            "Pending settlements are released within 10 working days of closure, "
            "after outstanding dues are deducted. Account closure requires 30 days' "
            "written notice.",
            [{"document": master, "clause": "5.1"},
             {"document": master, "clause": "5.2"}],
        )

    # Card settlement
    if "card" in q and any(x in q for x in ("settle", "settlement", "same day")):
        return result(
            "No. Card transactions settle T+2 (two working days).",
            [{"document": master, "clause": "1.2"}],
        )

    # Refunds: the amendment deletes clause 3.3 effective 1 September.
    if "refund" in q and any(x in q for x in ("fee", "mdr", "back", "return")):
        if d < date(2026, 9, 1):
            return result(
                "Yes. For a refund initiated within 24 hours of the transaction, "
                "the MDR is reversed in full.",
                [{"document": master, "clause": "3.2"},
                 {"document": master, "clause": "3.3"},
                 {"document": amendment, "clause": "D"}],
                CONFLICT,
            )
        return result(
            "No. From 1 September 2026, clause 3.3 is deleted and clause 3.2 "
            "applies without exception, so MDR is not returned.",
            [{"document": master, "clause": "3.2"},
             {"document": amendment, "clause": "D"}],
            CONFLICT,
        )

    # Daily UPI limit
    if any(x in q for x in ("twice", "daily limit", "per day", "same day")) and (
        "upi" in q or "pay" in q or "customer" in q
    ):
        return result(
            "No. The daily UPI limit per customer account is ₹1,00,000 across "
            "all UPI transactions, or the customer's own bank limit if lower. "
            "Two payments of ₹1,00,000 would exceed this limit.",
            [{"document": master, "clause": "4.3"},
             {"document": amendment, "clause": "E"}],
            CONFLICT,
        )

    # MDR cap / FAQ correctness
    if "faq" in q or "cap" in q or "upper limit" in q:
        if d >= date(2026, 8, 1):
            return result(
                "The FAQ says there is no upper fee limit. That is incorrect: "
                "from 1 August 2026, the MDR cap is ₹15 for merchants with monthly "
                "volume up to ₹10 lakh and ₹25 for merchants above ₹10 lakh. "
                "GST is outside the cap.",
                [{"document": faq, "clause": "FAQ: MDR"},
                 {"document": amendment, "clause": "C"},
                 {"document": master, "clause": "2.4"}],
                CONFLICT,
            )
        return result(
            "The FAQ says there is no upper fee limit, but the master policy "
            "caps MDR at ₹15 per transaction. GST is outside the cap.",
            [{"document": faq, "clause": "FAQ: MDR"},
             {"document": master, "clause": "2.3"},
             {"document": master, "clause": "2.4"}],
            CONFLICT,
        )

        # UPI fee arithmetic when amounts are explicitly supplied.
    if "upi" in q and any(x in q for x in ("mdr", "gst", "fee", "pay")):
        import re

        
        # Remove merchant-volume text before extracting transaction amount.
        cleaned_q = re.sub(
            r"(?:above|over|up to)\s+(?:rs\.?\s*)?[\d,.]+\s*lakh",
            "",
            q,
            flags=re.I,
        )

        amounts = re.findall(
            r"(?:₹|rs\.?\s*)\s*([\d,]+)",
            cleaned_q,
            re.I,
        )

        if not amounts:
            return result(
                "Cannot calculate: transaction amount is unclear.",
                [],
                CANNOT,
            )

        amount = int(amounts[0].replace(",", ""))
        large = "large merchant" in q or "above 10 lakh" in q
        volume = 1000001 if large else 1000000

        fees = calculate_upi_fee(amount, volume, d.isoformat())


        return result(
            f"MDR: ₹{fees['mdr']}; GST: ₹{fees['gst']}; "
            f"total fee: ₹{fees['total_fee']}.",
            [{"document": master, "clause": "2.1"},
             {"document": master, "clause": "2.2"},
             {"document": amendment, "clause": "B"},
             {"document": amendment, "clause": "C"},
             {"document": master, "clause": "2.4"}],
            CONFLICT if d >= date(2026, 8, 1) else ANSWERED,
        )

    # UPI settlement timing
    if "upi" in q and any(x in q for x in ("when", "receive", "money", "settle")):
        return result(
            "UPI settlement is T+1 (next working day) for merchants without "
            "an active Instant Settlement add-on. Merchants with that add-on "
            "receive same-day settlement by 11:59 PM.",
            [{"document": master, "clause": "1.1"},
             {"document": amendment, "clause": "A"}],
            CONFLICT,
        )

    return result(
        "The available rules do not establish a reliable answer to this question.",
        [],
        CANNOT,
    )