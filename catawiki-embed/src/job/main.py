"""catawiki main file."""

import logging
from typing import Annotated

from result import is_err
from typer import Typer, Argument

from helpers import logger, compute, inputs, embeder, db


app = Typer(name="catawiki-embed")


@app.command()
def embed(
    type_: Annotated[str, Argument(envvar="TYPE")],
    model_name: Annotated[str, Argument(envvar="MODEL_NAME")],
    cache_path: Annotated[str, Argument(envvar="CACHE_PATH")],
) -> None:
    logger.init()
    if type_ not in ["image", "text"]:
        logging.info("data should be of type image or text")
        return

    model = embeder.get_model(model_name=model_name)
    if is_err(model):
        logging.error(model.err_value)
        return

    con = db.set_db_connection(
        cache_path=cache_path,
        model=model.ok_value,  # type: ignore
    )

    batches = inputs.get_data(
        con=con,
        type_=type_,
        model=model.ok_value,  # type: ignore
    )

    output = compute.set_embeddings(
        con=con,
        batches=batches,
        model=model.ok_value,  # type: ignore
    )

    if is_err(output):
        con.close()
        logging.error(output.err_value)
        return
    logging.info(output.ok_value)  # type: ignore

    output = compute.set_index(
        con=con,
        model=model.ok_value,  # type: ignore
    )
    if is_err(output):
        con.close()
        logging.error(output.err_value)
        return
    logging.info(output.ok_value)  # type: ignore
    con.close()


@app.command()
def helper() -> None:
    logger.init()
    pass


if __name__ == "__main__":
    app()
