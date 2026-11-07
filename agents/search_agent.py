from chroma_db_code.search import search_documents

def search_agent(question: str):
    docs = search_documents(question)
    found = len(docs) > 0
    return {"found": found, "documents": docs, "summary": docs[0][:500] if docs else ""}
