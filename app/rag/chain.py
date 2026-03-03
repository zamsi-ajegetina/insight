"""LangChain Retrieval and Generation pipeline."""

import json
from typing import List, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
# LCEL imports
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.documents import Document

from app.config import settings
from app.rag.ingest import get_embeddings


# Custom JSON parser to safely extract the LLM's JSON response
class JsonOutputParser(StrOutputParser):
    """Parses a string back into standard JSON, handling typical markdown fences."""
    
    def parse(self, text: str) -> dict:
        import re
        text = text.strip()
        
        # Try finding a JSON block using regex if it's embedded in text
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
                
        # Fallback if valid JSON wasn't found
        return {
            "answer": text.strip(),
            "citations": []
        }


def get_vectorstore() -> Chroma:
    """Initialize connection to the local Chroma vectorstore."""
    return Chroma(
        persist_directory=settings.CHROMA_PERSIST_DIR,
        embedding_function=get_embeddings(),
        collection_name="policy_docs"
    )


def format_docs(docs: List[Document]) -> str:
    """Format documents for the prompt context block."""
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown")
        section = doc.metadata.get("section", "General")
        
        formatted.append(
            f"--- Context {i} ---\n"
            f"Source: {source}\n"
            f"Section: {section}\n"
            f"Content:\n{doc.page_content}\n"
        )
    return "\n".join(formatted)


def build_rag_chain():
    """Build the LangChain LCEL RAG chain pipeline."""
    
    # 1. Initialize LLM
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.LLM_MODEL,
        temperature=0.1,  # Low temperature for factual, grounded answers
        max_tokens=settings.MAX_OUTPUT_TOKENS,
    )
    
    # 2. Define the Prompt with Guardrails
    system_prompt = (
        "You are a helpful company policy assistant for Meridian Technologies.\n"
        "Your role is to answer employee questions about company policies and procedures.\n\n"
        "STRICT RULES:\n"
        "1. ONLY answer questions about company policies and procedures based on the provided context.\n"
        "2. If the question is NOT about company policies or the context does not contain relevant information, respond EXACTLY with:\n"
        "   \"I can only answer questions about Meridian Technologies company policies and procedures. Your question appears to be outside this scope.\"\n"
        "3. ALWAYS cite your sources by referencing the document name and section.\n"
        "4. Keep answers concise but thorough — aim for 2-4 paragraphs maximum.\n"
        "5. If multiple policies are relevant, reference all of them.\n"
        "6. Do NOT make up information. If the context doesn't fully answer the question, say so.\n"
        "7. Format citations as [Source: document_name, Section: section_name].\n"
        "8. CRITICAL: For the document_name in your citations, you MUST ONLY use the EXACT filenames provided in the `Source:` field of the Context blocks below. DO NOT invent or guess document names.\n\n"
        "RESPONSE FORMAT:\n"
        "Provide your answer in the following JSON format ONLY:\n"
        "{{\n"
        "  \"answer\": \"Your detailed answer here with inline citations like [Source: pto-policy.md, Section: PTO Accrual Rates]\",\n"
        "  \"citations\": [\n"
        "    {{\n"
        "      \"document\": \"exact-filename-from-context.md\",\n"
        "      \"section\": \"Section Name\",\n"
        "      \"snippet\": \"Brief relevant quote from the source\"\n"
        "    }}\n"
        "  ]\n"
        "}}\n\n"
        "CONTEXT (retrieved policy documents):\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "EMPLOYEE QUESTION:\n{input}"),
    ])
    
    # 3. Handle Missing API Key scenario
    if not settings.GROQ_API_KEY:
        return None
        
    # 4. Build native LCEL chain
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": settings.RETRIEVAL_TOP_K}
    )
    
    # The pure LCEL way: Dict of inputs -> Prompt -> LLM -> StrOutputParser
    chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


def generate_answer(question: str) -> dict:
    """Entry point to run the RAG chain for a given user question."""
    
    if not settings.GROQ_API_KEY:
        return {
            "answer": "Error: GROQ_API_KEY is not configured.",
            "citations": []
        }
        
    chain = build_rag_chain()
    
    try:
        # Run the chain (LCEL pipeline expects a string as input)
        response = chain.invoke(question)
        
        # Parse the JSON string from the chain output
        parser = JsonOutputParser()
        parsed_result = parser.parse(response)
        
        return parsed_result
        
    except Exception as e:
        return {
            "answer": f"An error occurred while generating the answer: {str(e)}",
            "citations": []
        }
