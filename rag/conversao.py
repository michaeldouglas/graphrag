import ollama
import psycopg

from docling.document_converter import DocumentConverter

# =========================================
# PostgreSQL Connection
# =========================================
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="ragdb",
    user="rag",
    password="rag"
)

cursor = conn.cursor()

# =========================================
# Create extension
# =========================================
cursor.execute("""
CREATE EXTENSION IF NOT EXISTS vector;
""")

# =========================================
# Create table
# =========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(768)
);
""")

conn.commit()

# =========================================
# PDF Extraction
# =========================================
converter = DocumentConverter()
result = converter.convert("arquivo.pdf")
text = result.document.export_to_markdown()

print(text)

# =========================================
# Chunking
# =========================================


def split_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> list[str]:

    chunks: list[str] = []

    for i in range(0, len(text), chunk_size - overlap):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks


chunks = split_text(text)

# =========================================
# Generate embeddings
# =========================================
for chunk in chunks:
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=chunk
    )

    embedding = response["embedding"]

    # =========================================
    # Insert into PostgreSQL
    # =========================================
    cursor.execute(
        """
        INSERT INTO documents (content, embedding)
        VALUES (%s, %s)
        """,
        (chunk, embedding)
    )

conn.commit()

print("Embeddings salvos com sucesso!")

# =========================================
# Close connection
# =========================================
cursor.close()
conn.close()
