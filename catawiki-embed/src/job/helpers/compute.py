"""catawiki embedding helper."""

from typing import Iterator

import duckdb
from result import Result, Ok
from sentence_transformers import SentenceTransformer

from helpers import embeder


def set_embeddings(
    batches: Iterator[list],
    model: SentenceTransformer,
    con: duckdb.DuckDBPyConnection,
) -> Result[str, str]:
    model_name = embeder.get_model_name(model=model)
    existing_ids = set(
        con.execute(query=f"SELECT id FROM embeddings_{model_name}")
        .fetch_df()["id"]
        .tolist()
    )

    query = open("sql/set_embeddings.sql", mode="r").read().format(
        model=model_name,
    )

    for batch in batches:
        filtered_batch = [row for row in batch if row[0] not in existing_ids]

        if len(filtered_batch) == 0:
            continue

        embeddings = model.encode(
            convert_to_numpy=True,
            sentences=[row[1] for row in filtered_batch],
        )

        parameters = [
            (row[0], embedding) for row, embedding in zip(filtered_batch, embeddings)
        ]
        con.executemany(query=query, parameters=parameters)
        existing_ids.update(row[0] for row in filtered_batch)

    return Ok("embeddings successfully computed")


def set_index(
    model: SentenceTransformer,
    con: duckdb.DuckDBPyConnection,
) -> Result[str, str]:
    model_name = embeder.get_model_name(model=model)
    con.execute(f"DROP INDEX IF EXISTS hnsw_idx_{model_name};")
    con.execute(query=open("./sql/set_index.sql", mode="r").read().format(model=model_name))
    return Ok("hnsw index successfully computed")
