import ollama
import psycopg

from psycopg import sql

# =========================================================
# PostgreSQL Connection
# =========================================================

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="ragdb",
    user="rag",
    password="rag"
)

cursor = conn.cursor()

# =========================================================
# OPERATORS
# =========================================================

OPERATORS = {
    "1": ("COSINE DISTANCE", "<=>"),
    "2": ("EUCLIDEAN DISTANCE", "<->"),
    "3": ("INNER PRODUCT", "<#>")
}

# =========================================================
# SEARCH FUNCTION
# =========================================================


def search_documents(question: str, operator: str):

    print(f"\nPergunta: {question}")

    # =========================================
    # Generate embedding
    # =========================================

    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=question
    )

    query_embedding = str(response["embedding"])

    # =========================================
    # Safe operator mapping
    # =========================================

    operator_sql = {
        "<=>": sql.SQL("<=>"),
        "<->": sql.SQL("<->"),
        "<#>": sql.SQL("<#>")
    }[operator]

    # =========================================
    # Dynamic SQL Query
    # =========================================

    query = sql.SQL("""
    SELECT
        content,
        embedding {} %s::vector AS distance
    FROM documents
    ORDER BY distance
    LIMIT 3;
    """).format(operator_sql)

    # =========================================
    # Execute Query
    # =========================================

    cursor.execute(query, (query_embedding,))

    results = cursor.fetchall()

    # =========================================
    # Results
    # =========================================

    print("\n========== RESULTADOS ==========\n")

    for index, row in enumerate(results, start=1):

        print(f"Resultado #{index}")
        print(f"Distance: {row[1]}")

        print("\nConteúdo:")
        print(row[0])

        print("\n-----------------------------\n")


# =========================================================
# MENU
# =========================================================

while True:

    print("\n==============================")
    print(" BUSCA VETORIAL COM PGVECTOR ")
    print("==============================")

    print("\nEscolha o tipo de busca:\n")

    print("1 - Cosine Distance (<=>)")
    print("2 - Euclidean Distance (<->)")
    print("3 - Inner Product (<#>)")
    print("0 - Sair")

    option = input("\nDigite a opção: ")

    if option == "0":
        break

    if option not in OPERATORS:

        print("\nOpção inválida!")
        continue

    question = input("\nDigite sua pergunta: ")

    operator_name, operator = OPERATORS[option]

    print(f"\nUsando {operator_name} ({operator})")

    search_documents(question, operator)

# =========================================================
# CLOSE CONNECTION
# =========================================================

cursor.close()
conn.close()

print("\nConexão encerrada.")
