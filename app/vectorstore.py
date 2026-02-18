from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters  import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "policies"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

PDF_NAME = "handbook.pdf"


def build_vectorstore():
    """
    Build (or rebuild) the vectorstore from handbook.pdf.
    Run this once during setup or whenever the PDF changes.
    """

    pdf_path = DATA_DIR / PDF_NAME
    if not pdf_path.exists():
        raise FileNotFoundError(f"Policy PDF not found: {pdf_path}")

    print(f"Loading PDF: {pdf_path}")
    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    print("Splitting text into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    print("Creating embeddings with OpenAI...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    print("Building Chroma vectorstore...")
    VECTORSTORE_DIR.mkdir(exist_ok=True)
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
    )

    print(f"Vectorstore created at: {VECTORSTORE_DIR}")


def get_vectorstore():
    """
    Load the existing vectorstore for retrieval.
    Used by the docs agent during query time.
    """
    if not VECTORSTORE_DIR.exists():
        raise RuntimeError(
            "Vectorstore not found. Run build_vectorstore() first."
        )

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    return Chroma(
        embedding_function=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
    )

if __name__ == "__main__":
    build_vectorstore()