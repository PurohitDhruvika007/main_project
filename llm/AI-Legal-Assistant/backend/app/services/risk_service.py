from app.services.llm_service import generate_answer


def analyze_risks(context: str) -> str:

    if not context or not context.strip():
        return (
            "No document content was provided "
            "for risk analysis."
        )

    prompt = """
Analyze the legal document below and identify the IMPORTANT
CLAUSES and POTENTIAL RISK POINTS that a person should carefully
review before accepting or signing the agreement.

Use ONLY information explicitly stated in the document.

IMPORTANT RULES:

1. Do not invent any clause, risk, penalty, amount, date,
   obligation, restriction, or condition.

2. Do not use outside legal knowledge.

3. A risk point must be based on an actual clause or condition
   present in the document.

4. Do not assume that every unusual clause is legally invalid.

5. Explain why a clause may deserve attention based only on
   what the document states.

6. Pay particular attention to clauses involving:
   - Payments or financial obligations
   - Penalties or late fees
   - Termination conditions
   - Notice periods
   - Confidentiality
   - Intellectual property
   - Liability
   - Indemnity
   - Restrictions
   - Renewal conditions
   - Dispute resolution
   - Governing law
   - Non-compete or similar restrictions
   - Security deposits
   - Refund conditions
   - Important deadlines
   - Automatic renewal
   - Other significant conditions

7. Do not create a risk merely because a category is not
   mentioned in the document.

8. Do not repeat the same clause as multiple risk points.

9. If a clause is important but not necessarily risky, it may
   be listed under IMPORTANT CLAUSES instead of POTENTIAL RISKS.

10. Keep the explanation simple and easy to understand.

11. Do not provide general legal advice.

12. Do not say that a clause is illegal unless the document
    itself explicitly says so.

13. Clearly distinguish between an IMPORTANT CLAUSE and a
    POTENTIAL RISK POINT.

14. If there are no clearly identifiable potential risks,
    write:
    "No specific potential risk points were clearly identified
    from the provided document."

15. If there are no particularly important clauses beyond
    normal agreement terms, write:
    "No additional important clauses were clearly identified
    from the provided document."

Return EXACTLY this structure:

IMPORTANT CLAUSES:

1. Clause/Topic:
   Explanation:
   Why it deserves attention:

2. Clause/Topic:
   Explanation:
   Why it deserves attention:

POTENTIAL RISK POINTS:

1. Risk/Clause:
   What the document says:
   Why it may be a concern:

2. Risk/Clause:
   What the document says:
   Why it may be a concern:

OVERALL ATTENTION:

Give a short 2-4 sentence explanation of the most important
things the user should carefully review in the document.

DOCUMENT:

"""

    prompt += context

    return generate_answer(
        context=context,
        question=prompt,
        max_new_tokens=400
    )
