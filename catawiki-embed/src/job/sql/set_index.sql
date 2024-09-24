CREATE INDEX hnsw_idx_{model} ON embeddings_{model} USING HNSW (vec) WITH (metric = 'cosine');
