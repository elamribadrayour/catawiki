"""catawiki search app."""

import pandas
import streamlit

from helpers import db, embeder


streamlit.title("Search For Catawiki")


database = db.get_db_connection()
# image_model = embeder.get_model(model_name="clip-ViT-B-32")
text_model = embeder.get_model(model_name="multi-qa-mpnet-base-cos-v1")


categories: list[str] = database.query(query="SELECT DISTINCT category_name FROM products ORDER BY 1").fetchdf()["category_name"].tolist()
category = streamlit.selectbox(
    label="choose a category",
    options=categories,
)
streamlit.dataframe(
    data=database.query(query=f"SELECT * FROM products WHERE category_name = '{category}'").fetchdf(),
)

text = streamlit.text_input(label="what are you looking for ?")
if len(text) == 0:
    streamlit.stop()

embedding = embeder.get_embedding(text=text, _model=text_model)

query = f"""
SELECT
    e.id,
    array_cosine_similarity(e.vec, ARRAY{embedding}::FLOAT[{embeder.get_model_output_size(model=text_model)}]) AS similarity,
    p.title AS name,
    p.url AS url,
    p.thumbImageUrl AS src,
    ROW_NUMBER() OVER (PARTITION BY e.id) AS rn
FROM embeddings_{embeder.get_model_name(model=text_model)} AS e
LEFT JOIN products AS p ON e.id = p.id
WHERE similarity > 0.2
ORDER BY similarity DESC
LIMIT 100
"""


rows: pandas.DataFrame = database.query(query=query).fetchdf()
streamlit.dataframe(rows)

columns = streamlit.columns(4)
for i, row in rows.iterrows():
    src = row["src"]
    url = row["url"]
    caption = str(row["id"]) + " - " + row["name"][:10].lower() + "..."

    columns[int(i) % 4].markdown(
        body=f"""
<div style="text-align: center;">
    <a href="{url}" target="_blank">
        <img src="{src}" style="width:150px; height:150px; object-fit: cover;">
    </a>
    <p style="margin-top: 10px; font-size: 16px; color: #555;">{caption}</p>
</div>
""",
        unsafe_allow_html=True,
    )
