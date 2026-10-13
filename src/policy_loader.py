from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "ai-2-data"

DOCUMENTS = {
    "policy_master_v1.md": DATA_DIR / "policy_master_v1.md",
    "circular_2026_08_amendment.md": DATA_DIR / "circular_2026_08_amendment.md",
    "merchant_faq_2026-03.md": DATA_DIR / "merchant_faq_2026-03.md",
}


def load_documents():
    """Load policy sources without inventing missing clauses."""
    documents = {}

    for name, path in DOCUMENTS.items():
        if not path.exists():
            raise FileNotFoundError(f"Required policy document missing: {path}")
        documents[name] = path.read_text(encoding="utf-8-sig")

    return documents