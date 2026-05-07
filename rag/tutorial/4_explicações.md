# Busca Vetorial com pgvector

## O que é busca vetorial?

Na busca vetorial, textos são transformados em vetores numéricos chamados embeddings.

Esses vetores representam semanticamente o conteúdo do texto.

Exemplo:

- "gato"
- "felino"
- "animal doméstico"

Possuem embeddings próximos no espaço vetorial.

---

# Como funciona no RAG

Fluxo simplificado:

1. O documento é transformado em embeddings
2. Os embeddings são armazenados no banco vetorial
3. A pergunta do usuário também vira embedding
4. O banco compara vetores
5. Os vetores mais próximos são recuperados

---

# Exemplo de consulta

```sql
SELECT
    content,
    embedding <=> %s AS distance
FROM documents
ORDER BY distance
LIMIT 3;
```

Nesse exemplo:

- `%s` representa o embedding da pergunta
- `<=>` calcula a distância vetorial
- os menores valores representam maior similaridade

---

# Operadores do pgvector

| Operador | Métrica            | Descrição                               |
| -------- | ------------------ | --------------------------------------- |
| `<->`    | Euclidean Distance | Mede distância geométrica entre vetores |
| `<=>`    | Cosine Distance    | Mede similaridade angular               |
| `<#>`    | Inner Product      | Mede produto interno entre vetores      |

---

# 1. Euclidean Distance (`<->`)

## Como funciona

Calcula a distância geométrica entre dois vetores.

Quanto menor a distância:

- mais próximos os vetores estão

## Fórmula

distância = raiz quadrada da soma das diferenças ao quadrado

## Características

- considera magnitude
- sensível ao tamanho do vetor
- comum em problemas geométricos

## Exemplo SQL

```sql
SELECT
    content,
    embedding <-> %s AS distance
FROM documents
ORDER BY distance
LIMIT 3;
```

---

# 2. Cosine Distance (`<=>`)

## Como funciona

Mede o ângulo entre vetores.

Muito utilizada em NLP e RAG.

## Características

- ignora magnitude
- foca direção semântica
- excelente para embeddings textuais

## Vantagem no RAG

Dois textos semanticamente parecidos geralmente apontam para direções semelhantes no espaço vetorial.

## Exemplo SQL

```sql
SELECT
    content,
    embedding <=> %s AS distance
FROM documents
ORDER BY distance
LIMIT 3;
```

---

# 3. Inner Product (`<#>`)

## Como funciona

Calcula o produto interno entre vetores.

Muito utilizado em:

- recomendações
- ranking
- sistemas ANN

## Características

- favorece vetores com maior magnitude
- extremamente rápido
- muito usado com embeddings normalizados

## Exemplo SQL

```sql
SELECT
    content,
    embedding <#> %s AS distance
FROM documents
ORDER BY distance
LIMIT 3;
```

---

# Qual usar no RAG?

Na maioria dos casos de NLP e RAG:

## Recomendado

Cosine Distance (`<=>`)

Porque:

- embeddings textuais funcionam melhor angularmente
- reduz impacto da magnitude
- melhora similaridade semântica

---

# Resumo visual

| Métrica       | Melhor para            |
| ------------- | ---------------------- |
| Euclidean     | Distância geométrica   |
| Cosine        | Similaridade semântica |
| Inner Product | Ranking e performance  |

---

# Conclusão

A busca vetorial é o núcleo de sistemas RAG.

Entender como as métricas funcionam é essencial para:

- melhorar recuperação
- reduzir hallucination
- aumentar relevância
- construir sistemas mais eficientes
