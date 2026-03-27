from typing import Generator

import ollama

from app import config


_PROMPT_TEMPLATE = """\
You are a knowledgeable assistant. Answer the question using ONLY the context provided below.
Cite sources inline using their reference numbers like [1], [2], etc.
If the answer is not in the context, say "I don't have enough information in my knowledge base to answer that."

Context:
{context}

Question: {question}

Answer (cite sources as [1], [2], etc.):"""


def build_prompt(question: str, context_chunks: list[dict]) -> str:
    context_parts = []
    for i, chunk in enumerate(context_chunks, 1):
        context_parts.append(f"[{i}] Source: {chunk['source']}\n{chunk['text']}")
    context = "\n\n".join(context_parts)
    return _PROMPT_TEMPLATE.format(context=context, question=question)


def generate(question: str, context_chunks: list[dict]) -> Generator[str, None, None]:
    prompt = build_prompt(question, context_chunks)
    try:
        stream = ollama.chat(
            model=config.OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        for chunk in stream:
            delta = chunk["message"]["content"]
            if delta:
                yield delta
    except Exception as e:
        error = str(e)
        if "connection" in error.lower() or "refused" in error.lower():
            yield (
                "**Error:** Cannot connect to Ollama. "
                "Please run `ollama serve` and ensure the model has been pulled."
            )
        else:
            yield f"**Error:** {error}"
