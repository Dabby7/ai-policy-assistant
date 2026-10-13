
import json
from src.assistant import ask


def main():
    with open("eval.json", encoding="utf-8") as f:
        cases = json.load(f)

    passed = 0
    print(f"{'No.':<5} {'Status':<8} {'Answer':<8} {'Citation':<10}")

    for i, case in enumerate(cases, 1):
        result = ask(case["question"], case["as_of_date"])
        answer_ok = case["expected_contains"].lower() in result["answer"].lower()
        status_ok = case["expected_status"] == result["status"]
        citation_ok = any(
            case["expected_citation"] == citation["document"]
            for citation in result["citations"]
        )

        ok = answer_ok and status_ok and citation_ok
        passed += int(ok)

        print(
            f"{i:<5} "
            f"{'PASS' if status_ok else 'FAIL':<8} "
            f"{'PASS' if answer_ok else 'FAIL':<8} "
            f"{'PASS' if citation_ok else 'FAIL':<10}"
        )

    print(f"\nScore: {passed}/{len(cases)} ({passed / len(cases) * 100:.1f}%)")


if __name__ == "__main__":
    main()
