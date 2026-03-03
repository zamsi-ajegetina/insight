# AI Tooling

This document describes the AI tools used during the development of this RAG Policy Q&A application.

## Tools Used

### 1. Antigravity (AI Coding Assistant)

**Role**: Primary development assistant throughout the project.

**How it was used**:
- Scaffolded the project structure and configuration files
- Generated synthetic company policy documents for the corpus
- Implemented the RAG pipeline (ingestion, retrieval, generation)
- Built the Flask web application and chat UI
- Created the evaluation framework and evaluation questions
- Wrote documentation (README, design docs)
- Set up the GitHub Actions CI/CD workflow

**What worked well**:
- Rapid scaffolding of the entire project from a requirements PDF
- Generating realistic and detailed policy documents that form a coherent corpus
- Writing structured code with proper error handling and configuration management
- Creating a polished chat UI with modern design

**What didn't work as well**:
- Had to iterate on prompt engineering for the guardrails to get consistent JSON output from the LLM
- Initial chunking strategy needed refinement to handle edge cases with very short or very long sections

### 2. Groq API (LLM Inference)

**Role**: Backend LLM for answer generation and evaluation (LLM-as-judge).

**How it was used**:
- Generates answers to policy questions with structured JSON output
- Evaluates groundedness of answers during evaluation

**What worked well**:
- Fast inference times (1-3 seconds per query)
- Free tier provides sufficient rate limits for development and evaluation
- Good at following structured output instructions

## Summary

The primary AI tool used was an AI coding assistant (Antigravity), which accelerated development significantly. The Groq API serves as the LLM backbone for the application itself. All code was reviewed and understood before integration.
