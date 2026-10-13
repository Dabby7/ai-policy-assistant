# Design Decisions

1. The August circular overrides master-policy clauses it explicitly amends.
2. General amendments take effect on 1 August 2026; the refund exception is removed on 1 September 2026.
3. Fee calculations use Python Decimal arithmetic.
4. GST is 18% of MDR and is outside the MDR cap.
5. Conflicting sources produce CONFLICT_RESOLVED with an explanation.
6. Unsupported questions produce CANNOT_ANSWER rather than invented facts.
7. Keyword-based routing was chosen to keep the implementation offline and reproducible.
