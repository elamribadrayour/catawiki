"""catawikip embed embeder helper."""

from result import Result, Ok, Err
from sentence_transformers import SentenceTransformer


def get_model(model_name: str) -> Result[SentenceTransformer, str]:
    try:
        return Ok(SentenceTransformer(model_name_or_path=model_name))
    except Exception:
        return Err(f"Model not found: model_name={model_name}")


def get_model_name(model: SentenceTransformer) -> str:
    model_name = model._first_module().auto_model.config._name_or_path
    return model_name.split("/")[1].replace("-", "_")


def get_model_output_size(model: SentenceTransformer) -> int:
    size = model.get_sentence_embedding_dimension()
    return size  # type: ignore
