"""LangChain-based document ingestion pipeline for ChromaDB."""

import os
from pathlib import Path
from typing import List

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

from app.config import settings


def load_documents(corpus_dir: str) -> List[Document]:
    """Load all markdown documents from the corpus directory."""
    print(f"Loading documents from {corpus_dir}...")
    
    if not Path(corpus_dir).exists():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    # Load markdown files
    loader = DirectoryLoader(
        corpus_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    docs = loader.load()
    
    # Store filename in metadata (instead of full absolute path)
    for doc in docs:
        if "source" in doc.metadata:
            doc.metadata["source"] = Path(doc.metadata["source"]).name
            
    return docs


def split_documents(docs: List[Document]) -> List[Document]:
    """Split documents preserving markdown headers, then by size."""
    print("Splitting documents...")
    
    # 1. Split by Markdown headers 
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )
    
    header_splits = []
    for doc in docs:
        splits = markdown_splitter.split_text(doc.page_content)
        # Add original source metadata back to the header splits
        for split in splits:
            split.metadata["source"] = doc.metadata["source"]
        header_splits.extend(splits)
        
    # 2. Split by character limit if any section is too long
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    final_splits = text_splitter.split_documents(header_splits)
    
    # Clean up metadata (combine headers into a single 'section' field)
    for split in final_splits:
        # Build section title from headers
        headers = [
            v for k, v in split.metadata.items()
            if k.startswith('Header')
        ]
        if headers:
            split.metadata["section"] = " > ".join(headers)
        else:
            split.metadata["section"] = "General"
            
        # Optional: remove original Header keys to keep metadata clean
        for k in list(split.metadata.keys()):
            if k.startswith('Header'):
                del split.metadata[k]
                
    return final_splits


def get_embeddings() -> HuggingFaceEmbeddings:
    """Initialize HuggingFace embeddings (runs locally)."""
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )


def ingest_corpus() -> dict:
    """Main ingestion function: load, split, embed, and store."""
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    
    docs = load_documents(settings.CORPUS_DIR)
    if not docs:
        raise ValueError("No documents loaded.")
        
    splits = split_documents(docs)
    
    print(f"Loaded {len(docs)} documents. Split into {len(splits)} chunks.")
    print(f"Initializing embeddings ({settings.EMBEDDING_MODEL})...")
    
    embeddings = get_embeddings()
    
    print("Storing in ChromaDB...")
    # This automatically persists to disk
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=settings.CHROMA_PERSIST_DIR,
        collection_name="policy_docs"
    )
    
    count = vectorstore._collection.count()
    
    return {
        "files_processed": len(docs),
        "chunks_created": len(splits),
        "collection_count": count,
        "persist_dir": settings.CHROMA_PERSIST_DIR
    }


if __name__ == "__main__":
    result = ingest_corpus()
    print("Ingestion complete:")
    print(f"  Files processed: {result['files_processed']}")
    print(f"  Chunks created:  {result['chunks_created']}")
    print(f"  Total in collection: {result['collection_count']}")
