SELECT
    p.id, 
    p.title AS content
FROM products p
LEFT JOIN embeddings_{model} e ON p.id = e.id
WHERE e.id IS NULL