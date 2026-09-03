from openai import OpenAI

from retrieval import retrieve_chunks


client = OpenAI()


def answer_question(question: str):

    chunks = retrieve_chunks(
        question,
        limit=5
    )

    context_sections = []

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        context_sections.append(
            f"""
[S{index}]
Source: {chunk["source_name"]}
Page: {chunk["page_number"]}

{chunk["content"]}
"""
        )

    context = "\n".join(
        context_sections
    )


    instructions = """
You are an internal company knowledge assistant.

Answer using only the company documentation
supplied to you.

Rules:

1. Do not invent company policies.
2. If the documentation does not contain enough
   information, say that you do not know.
3. Cite statements using identifiers such as
   [S1] or [S2].
4. Keep answers concise and clear.
"""


    response = client.responses.create(
        model="gpt-5-mini",

        instructions=instructions,

        input=f"""
COMPANY DOCUMENTATION

{context}

EMPLOYEE QUESTION

{question}
"""
    )


    return {
        "answer": response.output_text,

        "sources": [
            {
                "source_name":
                    chunk["source_name"],

                "page_number":
                    chunk["page_number"],

                "similarity":
                    chunk["similarity"]
            }

            for chunk in chunks
        ]
    }