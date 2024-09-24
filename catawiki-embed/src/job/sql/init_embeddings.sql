CREATE TABLE IF NOT EXISTS embeddings_{model} (
    id INTEGER PRIMARY KEY,
    vec FLOAT [{size}],
);