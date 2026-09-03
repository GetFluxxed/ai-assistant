from retrieval import retrieve_chunks

#This script was a test for the LLM's response using Semantic Search

question = (
    "Can a customer get their money "
    "back if their product arrives broken?"
)


results = retrieve_chunks(question)


for result in results:

    print("\n----------------")

    print(
        result["source_name"],
        "Page",
        result["page_number"]
    )

    print(
        "Similarity:",
        result["similarity"]
    )

    print(
        result["content"]
    )
