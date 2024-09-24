"""catawiki embed duckdb helper."""

import os

import duckdb
from sentence_transformers import SentenceTransformer

from helpers import embeder


def set_table(con: duckdb.DuckDBPyConnection, model: SentenceTransformer) -> None:
    query = (
        open("./sql/init_embeddings.sql", mode="r")
        .read()
        .format(
            model=embeder.get_model_name(model=model),
            size=embeder.get_model_output_size(model=model),
        )
    )
    con.execute(query=query)


def set_db_connection(
    cache_path: str, model: SentenceTransformer
) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(database=os.path.join(cache_path, "data.duckdb"))

    for query in [
        "INSTALL vss;",
        "LOAD vss;",
        "SET hnsw_enable_experimental_persistence = TRUE;",
    ]:
        con.execute(query=query)
    set_table(con=con, model=model)  # type: ignore
    return con
