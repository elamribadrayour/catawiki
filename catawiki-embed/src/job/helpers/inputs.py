"""inputs data helpers for catawiki embed."""

import logging
import requests
from io import BytesIO
from typing import Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed

import duckdb
from PIL import Image
from result import Result, Ok, Err, is_err
from sentence_transformers import SentenceTransformer


from helpers import embeder


def get_image_from_url(url: str) -> Result[Image.Image, str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return Ok(image)
    except requests.exceptions.RequestException as e:
        Err(f"An error occurred while downloading the image: {e}")
    except IOError as e:
        Err(f"An error occurred while processing the image: {e}")

    return Err("An error occurred while getting the image")


def get_images_from_urls(urls: list[str]) -> list[Result[Image.Image, str]]:
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_image_from_url, url): url for url in urls}
        results = []
        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append(Err(f"An error occurred with {url}: {e}"))
        return results


def get_text(
    con: duckdb.DuckDBPyConnection, model: SentenceTransformer
) -> Iterator[list]:
    logging.info("get text data for embedding")
    model_name = embeder.get_model_name(model=model)
    query = open("sql/get_text_data.sql", mode="r").read().format(model=model_name)
    cursor = con.query(query=query)
    while True:
        batch = cursor.fetchmany(size=1000)
        if not batch:
            break
        yield batch


def get_image(
    con: duckdb.DuckDBPyConnection, model: SentenceTransformer
) -> Iterator[list]:
    logging.info("get image data for embedding")

    model_name = embeder.get_model_name(model=model)
    query = open("sql/get_image_data.sql", mode="r").read().format(model=model_name)
    cursor = con.query(query=query)
    while True:
        batch = cursor.fetchmany(size=2)
        if not batch:
            break
        output = list()
        urls = [row[1] for row in batch]
        download_results = get_images_from_urls(urls=urls)
        for i, result in enumerate(download_results):
            if is_err(result):
                continue
            output.append((batch[i][0], result.ok_value))  # type: ignore
        yield output


def get_data(
    con: duckdb.DuckDBPyConnection, model: SentenceTransformer, type_: str
) -> Iterator[list]:
    if type_ == "text":
        return get_text(con=con, model=model)
    if type_ == "image":
        return get_image(con=con, model=model)
    raise ValueError("Type should be text of image")
