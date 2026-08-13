import sys
import json
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.rag_pipeline import RAGAssistant


QUESTIONS = [
    {
        "id": 1,
        "category": "Cyclone / Hurricane",
        "question": "What should I do during a hurricane?"
    },
    {
        "id": 2,
        "category": "Cyclone / Hurricane",
        "question": "Where should I take shelter during a hurricane?"
    },
    {
        "id": 3,
        "category": "Cyclone / Hurricane",
        "question": "What should I do after a hurricane?"
    },
    {
        "id": 4,
        "category": "Earthquake",
        "question": "What should I do during an earthquake if I am indoors?"
    },
    {
        "id": 5,
        "category": "Earthquake",
        "question": "What should I do if I am outside during an earthquake?"
    },
    {
        "id": 6,
        "category": "Earthquake",
        "question": "What should I do after an earthquake?"
    },
    {
        "id": 7,
        "category": "Flood",
        "question": "What should I do when there is a flood warning?"
    },
    {
        "id": 8,
        "category": "Flood",
        "question": "How can I stay safe around floodwater?"
    },
    {
        "id": 9,
        "category": "Flood",
        "question": "What should I do after a flood?"
    },
    {
        "id": 10,
        "category": "Out-of-Scope",
        "question": "What is the capital of France?"
    }
]


def main():

    print("=" * 70)
    print("DISASTER MANAGEMENT RAG - EVALUATION")
    print("=" * 70)

    print("\nInitializing RAG Assistant...")

    assistant = RAGAssistant(top_k=3)

    results = []

    for item in QUESTIONS:

        print("\n" + "-" * 70)
        print(f"Question {item['id']}")
        print(f"Category: {item['category']}")
        print(f"Question: {item['question']}")
        print("-" * 70)

        try:

            result = assistant.ask(item["question"])

            evaluation_result = {
                "id": item["id"],
                "category": item["category"],
                "question": item["question"],
                "answer": result["answer"],
                "sources": result["sources"]
            }

            results.append(evaluation_result)

            print("\nANSWER:")
            print(result["answer"])

            print("\nSOURCES:")

            if result["sources"]:

                for source in result["sources"]:

                    print(
                        f"- {source['source']} | "
                        f"Page {source['page']} | "
                        f"Score {source['score']:.4f}"
                    )

            else:

                print("No relevant sources found.")

        except Exception as error:

            print("\nERROR:")
            print(error)

            results.append(
                {
                    "id": item["id"],
                    "category": item["category"],
                    "question": item["question"],
                    "answer": None,
                    "sources": [],
                    "error": str(error)
                }
            )

    # ---------------------------------------------------------
    # SAVE EVALUATION RESULTS
    # ---------------------------------------------------------

    output_path = PROJECT_ROOT / "evaluation" / "evaluation_results.json"

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)

    print(
        f"\nResults saved to: {output_path}"
    )

    print(
        f"Total questions evaluated: {len(results)}"
    )


if __name__ == "__main__":
    main()