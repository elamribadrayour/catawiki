"""catawiki main file."""

import logging
from typing import Annotated

from result import is_err
from typer import Typer, Argument

from helpers import logger, scraper


app = Typer(name="catawiki-scrape")


@app.command()
def scrape(
    cache_path: Annotated[str, Argument(envvar="CACHE_PATH")],
) -> None:
    logger.init()
    logging.info("scraping data from catawiki")

    output = scraper.get_data(
        cache_path=cache_path,
    )

    if is_err(output):
        logging.error(output.err_value)
        return


@app.command()
def helper() -> None:
    logger.init()


if __name__ == "__main__":
    app()
