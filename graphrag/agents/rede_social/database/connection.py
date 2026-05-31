from falkordb import FalkorDB

cliente = FalkorDB(
    host="localhost",
    port=6379
)

grafo = cliente.select_graph("rede_social")
