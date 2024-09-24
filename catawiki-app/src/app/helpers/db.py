"""catawiki app duckdb helper."""

import os

import duckdb
import streamlit

import helpers.env


@streamlit.cache_resource()
def get_db_connection() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(database=os.path.join(helpers.env.cache_path, "data.duckdb"))
    for query in [
        "INSTALL vss;",
        "LOAD vss;",
        "SET hnsw_enable_experimental_persistence = TRUE;",
    ]:
        con.execute(query=query)
    return con
