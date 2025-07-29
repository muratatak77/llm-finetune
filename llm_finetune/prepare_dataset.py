# llm_finetune/prepare_dataset.py

import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.db import SessionLocal
from models.schema import Animal

# Initialize database session
session = SessionLocal()
qa_pairs = []

# Iterate over animals and their related tests/results
for animal in session.query(Animal).all():
    for test in animal.tests:
        # Format date safely
        test_date = test.test_date.strftime('%Y-%m-%d') if isinstance(test.test_date, datetime) else str(test.test_date)

        # Formulate the question
        question = (
            f"What are the results of the {test.test_type} test "
            f"performed on {animal.name} (a {animal.breed} {animal.species}) "
            f"on {test_date}?"
        )

        # Collect test result values
        if test.results:
            result_strings = [f"{r.parameter}: {r.value} {r.unit}" for r in test.results]
            answer = ", ".join(result_strings) + " <|endoftext|>"
        else:
            answer = "No results available. <|endoftext|>"

        # Append as instruction-output pair
        qa_pairs.append({"instruction": question, "output": answer})

# Write to JSON file
os.makedirs("llm_finetune/model_output", exist_ok=True)
with open("llm_finetune/model_output/qa_data.json", "w") as f:
    json.dump(qa_pairs, f, indent=2)

print(f"{len(qa_pairs)} QA pairs generated and saved to llm_finetune/model_output/qa_data.json.")
