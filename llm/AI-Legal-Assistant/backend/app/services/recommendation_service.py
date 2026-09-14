import re

from app.services.llm_service import generate_answer


def clean_recommendations(answer: str) -> str:

    if not answer:
        return (
            "No specific document-based recommendations "
            "were identified."
        )

    answer = answer.strip()

    forbidden_phrases = [
        "fair, reasonable, and appropriate",
        "fair and reasonable",
        "fair or reasonable",
        "fair, reasonable",
        "meets your goals",
        "meets the reader's goals",
        "meets the reader’s goals",
        "aligned with your goals",
        "aligned with the reader's goals",
        "aligned with the reader’s goals",
        "appropriate for your situation",
        "sufficient for your needs",
        "suitable for your needs"
    ]

    for phrase in forbidden_phrases:
        answer = re.sub(
            re.escape(phrase),
            "",
            answer,
            flags=re.IGNORECASE
        )

    answer = re.sub(
        r"\s+([,.])",
        r"\1",
        answer
    )

    answer = re.sub(
        r"[ \t]{2,}",
        " ",
        answer
    )

    answer = re.sub(
        r"\n[ \t]+",
        "\n",
        answer
    )

    answer = re.sub(
        r"\.\s*\.",
        ".",
        answer
    )

    answer = re.sub(
        r"\n{3,}",
        "\n\n",
        answer
    )

    return answer.strip()


def generate_recommendations(context: str) -> str:

    if not context or not context.strip():
        return (
            "No document content was provided "
            "for recommendation analysis."
        )

    prompt = """
Analyze ONLY the legal document provided below.

Your task is to provide exactly THREE important and practical
recommendations based strictly on facts, clauses, conditions,
rights, obligations, amounts, dates, deadlines, restrictions,
or procedures that are explicitly present in the document.

DOCUMENT-GROUNDING RULES:

1. Use ONLY information explicitly contained in the DOCUMENT.

2. Do NOT use any information from previous conversations,
previous documents, previous questions, examples, or memory.

3. Do NOT assume that the current document is similar to another
legal document.

4. Do NOT invent any facts, clauses, amounts, dates, percentages,
parties, rights, obligations, penalties, restrictions, or
conditions.

5. Every recommendation MUST be traceable to a specific statement
in the DOCUMENT.

6. Before writing each recommendation, identify the exact fact
or clause in the DOCUMENT that supports it.

7. If a fact is not present in the DOCUMENT, do not mention it.

8. Do not use examples from this instruction as facts about the
DOCUMENT. They are only examples of formatting and style.

9. Do not judge whether any term is fair, unfair, reasonable,
unreasonable, appropriate, inappropriate, sufficient, or
insufficient.

10. Do not provide generic legal advice.

11. Do not claim that a condition is missing or unclear unless
the DOCUMENT itself clearly indicates that.

12. When mentioning an amount, percentage, date, duration,
notice period, or other specific value, copy it accurately from
the DOCUMENT.

13. A recommendation should tell the reader what specific
document term they should review, confirm, understand, or pay
attention to.

14. Do not introduce information that cannot be found in the
DOCUMENT.

15. Do not mention any party, clause, or term that does not exist
in the DOCUMENT.

16. Do not repeat the same document term in multiple
recommendations.

17. If the document contains fewer than three obvious areas for
recommendation, use three different significant terms that are
actually present in the DOCUMENT rather than inventing new
information.

18. The recommendation must remain informational and
document-based.

GOOD RECOMMENDATION STYLE:

Topic:
The specific clause or term actually present in the document.

What the document says:
Accurately describe the relevant information from the document.

Recommendation:
Tell the reader what they should specifically review,
understand, verify, or confirm about that stated term.

IMPORTANT:

The following are examples ONLY. They are NOT facts about the
current document:

Example:
"Review the stated contribution amount and confirm that it
matches the agreed contribution."

Example:
"Review the stated profit-sharing ratio and confirm that you
understand the arrangement."

Example:
"Review the requirement for written consent and understand
when joint approval is required."

Never copy the facts from these examples into the answer unless
those exact facts are present in the DOCUMENT.

Return ONLY this structure:

KEY RECOMMENDATIONS:

1. Topic:
   What the document says:
   Recommendation:

2. Topic:
   What the document says:
   Recommendation:

3. Topic:
   What the document says:
   Recommendation:

IMPORTANT NOTE:

These recommendations are based only on the uploaded document
and are intended for general informational purposes. They are
not legal advice.

Do NOT generate any other sections.

DOCUMENT:

"""

    prompt += context

    answer = generate_answer(
        context=context,
        question=prompt,
        max_new_tokens=300
    )

    answer = clean_recommendations(answer)

    return answer
