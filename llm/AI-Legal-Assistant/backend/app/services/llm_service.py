from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "models/llm/legal-slm-500m-sft"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    dtype=torch.float32
)

model.eval()


def generate_answer(context: str, question: str, max_new_tokens: int = 100) -> str:

    # Keep the context small so the question and answer instruction
    # are not lost because of the model's context limit.
    context = context[:3000]

    prompt = f"""You are a legal document assistant.

Answer the question using only the information given in the legal document.
Give a short, simple and clear answer.
Do not invent information.

Legal Document:
{context}

Question: {question}

Answer:"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=700
    )

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    # Get only the newly generated tokens.
    input_length = inputs["input_ids"].shape[1]

    generated_tokens = output[0][input_length:]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    if "Answer:" in answer:
        answer = answer.split("Answer:", 1)[-1].strip()

    return answer
