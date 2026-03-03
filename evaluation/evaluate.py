#!/usr/bin/env python3
"""Evaluation script for the FastAPI+LangChain RAG application.

Measures:
1. Groundedness — Is the answer supported by the retrieved context?
2. Citation Accuracy — Do citations point to the correct source documents?
3. Latency — p50 and p95 response times
"""

import json
import sys
import time
from pathlib import Path
from statistics import median

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from app.config import settings

# In the FastAPI version, we test via the TestClient
from fastapi.testclient import TestClient
from app.main import app
from app.rag.chain import get_vectorstore

client = TestClient(app)

def load_eval_questions() -> list[dict]:
    """Load evaluation questions from JSON file."""
    eval_path = Path(__file__).parent / "eval_questions.json"
    with open(eval_path) as f:
        return json.load(f)


def evaluate_citation_accuracy(result: dict, expected_sources: list[str]) -> bool:
    """Check if any of the expected sources appear in the citations."""
    if not result.get("citations"):
        return False

    cited_docs = set()
    for c in result["citations"]:
        doc = c.get("document", "")
        cited_docs.add(doc.lower())

    return any(src.lower() in cited_docs for src in expected_sources)


def evaluate_groundedness(question: str, answer: str, context_chunks: list[dict]) -> float:
    """Use LLM-as-judge to evaluate if the answer is grounded in context."""
    if not settings.GROQ_API_KEY:
        return -1  # Skip if no API key

    from groq import Groq

    context_text = "\n\n".join(
        f"[{c.metadata.get('source', '')}] {c.page_content}" for c in context_chunks
    )

    judge_prompt = f"""You are an evaluation judge. Determine if the ANSWER is fully supported by the CONTEXT.

CONTEXT:
{context_text}

QUESTION: {question}

ANSWER: {answer}

Rate the groundedness on a scale of 0 to 1:
- 1.0: The answer is completely supported by the context. Every claim can be traced back.
- 0.5: The answer is partially supported. Some claims are supported, others are not.
- 0.0: The answer is not supported by the context at all, or contains fabricated information.

Respond with ONLY a JSON object: {{"score": <float>, "reason": "<brief reason>"}}
"""

    llm = Groq(api_key=settings.GROQ_API_KEY)
    try:
        completion = llm.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[{"role": "user", "content": judge_prompt}],
            temperature=0.0,
            max_tokens=200,
        )
        raw = completion.choices[0].message.content.strip()
        
        import re
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        parsed = json.loads(raw)
        return float(parsed.get("score", 0))
    except Exception as e:
        print(f"  ⚠ Groundedness judge error: {e}")
        return -1


def run_evaluation():
    """Run the full evaluation and output results."""
    questions = load_eval_questions()
    print(f"📋 Running evaluation on {len(questions)} questions (FastAPI version)...\n")
    
    # We need to manually retrieve context just for the groundedness judge
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": settings.RETRIEVAL_TOP_K})

    results = []
    latencies = []
    citation_correct = 0
    groundedness_scores = []

    for q in questions:
        qid = q["id"]
        question = q["question"]
        expected_sources = q["expected_sources"]
        topic = q["topic"]

        print(f"  [{qid:2d}/{len(questions)}] {question[:60]}...", end=" ", flush=True)

        # Measure latency (testing the actual FastAPI endpoint)
        start = time.time()
        
        # 1. Hit the API
        resp = client.post("/chat", json={"question": question})
        result = resp.json()
        
        elapsed = time.time() - start
        latencies.append(elapsed)

        # 2. Get the context chunks manually for the judge
        chunks = retriever.invoke(question)

        # 3. Evaluate citation accuracy
        cite_ok = evaluate_citation_accuracy(result, expected_sources)
        if cite_ok:
            citation_correct += 1

        # 4. Evaluate groundedness
        g_score = evaluate_groundedness(question, result.get("answer", ""), chunks)
        if g_score >= 0:
            groundedness_scores.append(g_score)

        status = "✅" if cite_ok else "❌"
        g_display = f"G:{g_score:.1f}" if g_score >= 0 else "G:skip"
        print(f"{status} {g_display} ({elapsed:.1f}s)")

        results.append({
            "id": qid,
            "question": question,
            "topic": topic,
            "answer": result.get("answer", ""),
            "citations": result.get("citations", []),
            "expected_sources": expected_sources,
            "citation_correct": cite_ok,
            "groundedness_score": g_score,
            "latency_seconds": round(elapsed, 3),
        })

    # Calculate metrics
    latencies_sorted = sorted(latencies)
    p50 = median(latencies_sorted) if latencies_sorted else 0
    p95_idx = int(len(latencies_sorted) * 0.95) - 1 if latencies_sorted else -1
    p95 = latencies_sorted[max(0, p95_idx)] if latencies_sorted else 0

    citation_pct = (citation_correct / len(questions)) * 100 if questions else 0
    avg_groundedness = (
        sum(groundedness_scores) / len(groundedness_scores)
        if groundedness_scores
        else 0
    )
    groundedness_pct = avg_groundedness * 100

    # Print summary
    print("\n" + "=" * 60)
    print("📊 EVALUATION RESULTS (FastAPI + LangChain)")
    print("=" * 60)
    print(f"  Questions evaluated:   {len(questions)}")
    print(f"  Citation Accuracy:     {citation_pct:.1f}% ({citation_correct}/{len(questions)})")
    print(f"  Groundedness:          {groundedness_pct:.1f}% (avg score: {avg_groundedness:.2f})")
    print(f"  Latency p50:           {p50:.2f}s")
    print(f"  Latency p95:           {p95:.2f}s")
    print("=" * 60)

    # Save results
    output = {
        "summary": {
            "total_questions": len(questions),
            "citation_accuracy_pct": round(citation_pct, 1),
            "groundedness_pct": round(groundedness_pct, 1),
            "latency_p50_seconds": round(p50, 3),
            "latency_p95_seconds": round(p95, 3),
        },
        "results": results,
    }

    output_path = Path(__file__).parent / "results_langchain.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n📁 Full results saved to {output_path}")
    return output


if __name__ == "__main__":
    run_evaluation()
