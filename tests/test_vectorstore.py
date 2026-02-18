from app.vectorstore import get_vectorstore

def test_vectorstore_real_retrieval_overtime():
    """
    Minimal real test:
    - Uses the already-built vectorstore
    - Calls get_vectorstore()
    - Performs a real similarity_search()
    - Confirms the returned text contains 'Overtime'
    """
    store = get_vectorstore()
    results = store.similarity_search("Overtime", k=1)

    assert len(results) >= 1
    assert "Overtime" in results[0].page_content