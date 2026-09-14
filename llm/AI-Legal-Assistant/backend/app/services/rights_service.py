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

STRICT ACCURACY RULES:

1. Every important clause and every risk point MUST be based
   directly on information present in the document.

2. NEVER claim that information is missing, unclear, unspecified,
   or not provided when the document explicitly provides that
   information.

3. NEVER invent a missing condition or create a risk because
   something is not mentioned unless the document itself clearly
   creates that issue.

4. An IMPORTANT CLAUSE is a significant condition, requirement,
   right, obligation, restriction, payment, deadline, procedure,
   or other term that deserves attention.

5. A POTENTIAL RISK POINT is a specific condition in the document
   that could create a concern for a party and therefore deserves
   careful review.

6. An important clause does NOT automatically mean it is a risk.

7. Do not describe a clearly stated clause as a "lack of clarity."

8. Do not claim that a clause may cause disputes unless there is
   a specific reason based on the wording or condition stated in
   the document.

9. Do not invent consequences that are not supported by the
   document.

10. Do not say that a clause is illegal, invalid, unfair, or
    unenforceable.

11. Do not use outside legal knowledge.

12. Do not provide general legal advice.

13. Do not repeat the same clause as multiple risk points.

14. Every risk point must accurately represent what the document
    actually says.

15. When mentioning an amount, date, percentage, duration,
    notice period, penalty, or other specific detail, copy it
    accurately from the document.

16. Pay particular attention to:
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

17. Do NOT create a risk merely because one of the above
    categories is absent.

18. If the document contains clearly defined terms, treat them
    as clearly defined.

19. Before producing the final answer, verify every risk point
    against the document context.

20. If there are no clearly identifiable potential risks, write:

    No specific potential risk points were clearly identified
    from the provided document.

21. If there are important clauses but no specific potential
    risks, list the important clauses and state that no specific
    potential risk points were clearly identified.

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
