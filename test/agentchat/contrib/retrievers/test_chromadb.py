import os
import pytest
from autogen.agentchat.contrib.retriever.retrieve_utils import (
    split_text_to_chunks,
    extract_text_from_pdf,
    split_files_to_chunks,
    get_files_from_dir,
    is_url,
)
from autogen.agentchat.contrib.retriever.chromadb import ChromaDB
try:
    import chromadb
except ImportError:
    skip = True
else:
    skip = False
    
test_dir = os.path.join(os.path.dirname(__file__), "test_files")

@pytest.mark.skipif(skip, reason="chromadb is not installed")
def test_chromadb():
    db_path = "/tmp/test_retrieve_utils_chromadb.db"
    client = chromadb.PersistentClient(path=db_path)
    if os.path.exists(db_path):
        vectorstore = ChromaDB(path=db_path, use_existing=True)
    else:
        vectorstore = ChromaDB(path=db_path)
    vectorstore.ingest_data(test_dir)
    
    assert client.get_collection("vectorstore")
    
    results = vectorstore.query(["autogen"])
    assert isinstance(results, dict) and any("autogen" in res[0].lower() for res in results.get("documents", []))