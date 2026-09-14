from app.services.llm_service import generate_answer


def simplify_document(context: str) -> str:

    if not context or not context.strip():
        return "No document content was provided."

    prompt = f"""
Summarize the following legal document in simple and easy-to-understand language.

LEGAL DOCUMENT:

{context}

Provide the summary using this structure:

Document Overview:
Briefly explain what this document is about.

Parties:
Identify the parties mentioned in the document.

Purpose:
Explain the main purpose of the agreement.

Important Terms:
List the important terms, conditions, amounts, dates, durations, and requirements stated in the document.

Rights and Obligations:
Explain the important rights and responsibilities of the parties.

Termination or Ending Conditions:
Explain how the agreement can end, if stated.

Governing Law:
Mention the governing law or jurisdiction if stated.

Important Note:
Mention that this is a simplified explanation of the provided document and not legal advice.

Use ONLY the information contained in the document.
Do not invent or assume any information.
"""

    return generate_answer(
        context=context,
        question=prompt,
        max_new_tokens=150
    )
