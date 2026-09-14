
import re
import httpx


# ---------------------------------------------------------
# llama.cpp persistent server
# ---------------------------------------------------------

LLAMA_SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"


# ---------------------------------------------------------
# Clean generated answer
# ---------------------------------------------------------

def clean_answer(answer: str) -> str:
    answer = answer.strip()

    prefixes = [
        "Answer:",
        "answer:",
        "Response:",
        "response:"
    ]

    for prefix in prefixes:
        if answer.startswith(prefix):
            answer = answer[len(prefix):].strip()

    stop_words = [
        "\nQuestion:",
        "\nLegal document:",
        "\nContext:",
        "\nAnswer:",
        "\nUser:",
        "\nAssistant:"
    ]

    for stop_word in stop_words:
        if stop_word in answer:
            answer = answer.split(stop_word, 1)[0].strip()

    answer = re.sub(r"\s+", " ", answer).strip()

    return answer


# ---------------------------------------------------------
# Extract useful sentence from retrieved context
# ---------------------------------------------------------

def extract_relevant_sentence(
    context: str,
    question: str
):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        context
    )

    question_words = set(
        re.findall(
            r"\b[a-zA-Z]{4,}\b",
            question.lower()
        )
    )

    best_sentence = None
    best_score = 0

    for sentence in sentences:
        sentence_words = set(
            re.findall(
                r"\b[a-zA-Z]{4,}\b",
                sentence.lower()
            )
        )

        score = len(
            question_words.intersection(
                sentence_words
            )
        )

        if score > best_score:
            best_score = score
            best_sentence = sentence.strip()

    if best_score >= 2:
        return best_sentence

    return None


# ---------------------------------------------------------
# Build legal assistant prompt
# ---------------------------------------------------------

def build_prompt(
    context: str,
    question: str
):
    system_message = """You are an AI legal document assistant.

Your task is to answer questions about an uploaded legal document.

IMPORTANT RULES:

1. Use ONLY the information contained in the provided document context.

2. Do not invent facts, names, dates, amounts, clauses, rights, duties, or obligations.

3. Do not use outside legal knowledge to answer the question.

4. If the answer is clearly present in the document, answer it directly.

5. If the document does not contain enough information, clearly say that the information is not available in the provided document.

6. For questions about amounts, provide the amount stated in the document.

7. For questions about dates or duration, provide the dates or duration stated in the document.

8. For questions about parties, identify the relevant party or parties from the document.

9. For questions about clauses, explain the relevant clause using simple language.

10. Keep the answer clear, concise, and easy to understand.

11. Do not make assumptions.

12. Do not give a generic legal answer when the document itself does not provide the information.

13. Answer only the user's question.

14. Do not repeat the entire document."""

    return {
        "messages": [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": f"""LEGAL DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

Answer the user's question using only the legal document context above."""
            }
        ],
        "temperature": 0,
        "top_p": 1,
        "max_tokens": 150
    }


# ---------------------------------------------------------
# Generate answer using persistent llama.cpp server
# ---------------------------------------------------------

def generate_with_model(
    context: str,
    question: str,
    max_new_tokens: int = 150
):
    payload = build_prompt(
        context=context,
        question=question
    )

    payload["max_tokens"] = max_new_tokens

    try:
        response = httpx.post(
            LLAMA_SERVER_URL,
            json=payload,
            timeout=300.0
        )

    except httpx.RequestError as e:
        raise RuntimeError(
            "Could not connect to llama.cpp server. "
            "Make sure llama-server.exe is running on port 8080."
        ) from e

    if response.status_code != 200:
        raise RuntimeError(
            f"llama.cpp server error "
            f"{response.status_code}: {response.text}"
        )

    data = response.json()

    try:
        answer = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise RuntimeError(
            f"Invalid response from llama.cpp server: {data}"
        )

    return clean_answer(answer)


# ---------------------------------------------------------
# Main answer function
# ---------------------------------------------------------

def generate_answer(
    context: str,
    question: str,
    max_new_tokens: int = 150
) -> str:

    if not context or not context.strip():
        return (
            "I could not find relevant information "
            "in the provided document."
        )

    if not question or not question.strip():
        return "Please provide a question."

    # Keep retrieved context limited
    # while preserving the existing RAG design.

    context = context[:8000]

    answer = generate_with_model(
        context=context,
        question=question,
        max_new_tokens=max_new_tokens
    )

    bad_answers = {
        "",
        "no",
        "no.",
        "yes",
        "yes.",
        "i don't know",
        "i do not know",
        "unknown",
        "not sure"
    }

    if answer.lower().strip() not in bad_answers:
        return answer

    # Fallback when model does not provide a useful answer

    relevant_sentence = extract_relevant_sentence(
        context=context,
        question=question
    )

    if relevant_sentence:
        return relevant_sentence

    return (
        "I could not find a clear answer "
        "in the provided document."
    )
