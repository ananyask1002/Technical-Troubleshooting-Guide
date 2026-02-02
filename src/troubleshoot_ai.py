"""
Technical Troubleshooting Guide
RAG-based IT Troubleshooting System
"""

from pathlib import Path
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI

# --------------------------------------------------
# Step 1: Load and preprocess logs & solutions
# --------------------------------------------------

def load_data():
    log_text = Path("data/error_logs.txt").read_text(encoding="utf-8")
    solution_text = Path("data/solutions.txt").read_text(encoding="utf-8")

    documents = []
    documents.extend([chunk.strip() for chunk in log_text.split("\n\n") if chunk.strip()])
    documents.extend([chunk.strip() for chunk in solution_text.split("\n\n") if chunk.strip()])

    return documents


# --------------------------------------------------
# Step 2: Create Vector Store
# --------------------------------------------------

def create_vector_store(documents):
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_texts(documents, embeddings)
    return vector_db


# --------------------------------------------------
# Step 3: Retrieve relevant context
# --------------------------------------------------

def retrieve_context(vector_db, query, k=3):
    results = vector_db.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in results])


# --------------------------------------------------
# Step 4: RAG-based Troubleshooting
# --------------------------------------------------

def troubleshoot_issue(query, context):
    prompt = f"""
You are an experienced IT support assistant.

Use the following past error logs and solutions to help resolve the issue.
Provide clear, step-by-step troubleshooting guidance.

Context:
{context}

User Issue:
{query}

Troubleshooting Steps:
"""

    llm = OpenAI(temperature=0.2)
    response = llm(prompt)
    return response


# --------------------------------------------------
# Step 5: Main execution
# --------------------------------------------------

if __name__ == "__main__":
    print("🔧 Technical Troubleshooting Guide 🔧\n")

    documents = load_data()
    vector_db = create_vector_store(documents)

    user_query = input("Describe the issue you are facing:\n> ")

    retrieved_context = retrieve_context(vector_db, user_query)
    solution = troubleshoot_issue(user_query, retrieved_context)

    print("\n✅ Suggested Troubleshooting Steps:\n")
    print(solution)
