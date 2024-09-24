"""catawiki app sentence transformers helper."""

import streamlit
from sentence_transformers import SentenceTransformer


@streamlit.cache_resource()
def get_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name_or_path=model_name)


def get_embedding(text: str, _model: SentenceTransformer) -> list:
    return _model.encode(
        sentences=text, show_progress_bar=False, convert_to_numpy=True
    ).tolist()


def get_model_name(model: SentenceTransformer) -> str:
    model_name = model._first_module().auto_model.config._name_or_path
    return model_name.split("/")[1].replace("-", "_")


def get_model_output_size(model: SentenceTransformer) -> int:
    size = model.get_sentence_embedding_dimension()
    return size  # type: ignore
