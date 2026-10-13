# AI Policy Assistant

An offline, date-aware question-answering assistant for merchant policy documents.

## Features
- Policy answers based on effective dates
- Conflict resolution between policy documents
- Source document and clause citations
- Deterministic MDR and GST calculations using Decimal
- CANNOT_ANSWER for unsupported questions
- Automated tests and a 12-question evaluation suite

## Requirements
Python 3.11+ recommended.

## Run
Install pytest:
python -m pip install pytest

Run tests:
python -m pytest -q

Run evaluation:
python evaluate.py

## Architecture
Policy documents are loaded locally. Rule-based question routing selects answers, date checks handle policy changes, and Python calculates fees.

## Limitations
Retrieval is rule-based, not semantic. Questions with unfamiliar wording may be misclassified. Review citations and evaluation results before relying on answers.
