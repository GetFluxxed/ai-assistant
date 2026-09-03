from rag import answer_question

#This script was a test for our RAG workflow and AI response

result = answer_question(
    "Can I refund a damaged $700 order?"
)


print("\nANSWER\n")

print(
    result["answer"]
)


print("\nSOURCES\n")

for source in result["sources"]:

    print(source)