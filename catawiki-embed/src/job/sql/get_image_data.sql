SELECT
    p.id, 
    p.thumbImageUrl AS content
FROM products p
LEFT JOIN embeddings_{model_name} e ON p.id = e.id
WHERE e.id IS NULL