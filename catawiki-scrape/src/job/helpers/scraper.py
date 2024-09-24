import os
import time
import json
import logging

import duckdb
import requests
from bs4 import BeautifulSoup
from result import Ok, Err, Result, is_err


def get_headers() -> dict:
    return {
        "dnt": "1",
        "priority": "u=0, i",
        "sec-fetch-user": "?1",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "document",
        "cache-control": "max-age=0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-site": "same-origin",
        "upgrade-insecure-requests": "1",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7",
        "referer": "https://www.catawiki.com/en/c/863-archaeology-natural-history",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "cookie": "absmartly_id=85ffa94b-687d-4d4a-a25e-02fc3f60fbc6; cw_ab=uPBtdFenRXy9RQtQxd9lBgAB; enable_marketing_cookies=true; enable_analytical_cookies=true; cookie_preferences_used_cta=accept_all; previously_logged_in=yes; _pxhd=f9c296338ccfd76135ffc4d269a7ccd6fb612ad8ba16b173346aac0b49324fd9:bf2ba1ed-7387-11ef-9875-dcf7102b73e1; cw_abcpbs=f8847887f55a4eb74bca30f02168da13; cw_sid=39387152819574ed832bf6d5637540900ea1d147c46ab340029814e51299cd97; cw_slidein_timer_started_at=1726772306770; rmb_disabled_at=1726772339117; view_mode=gallery",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    }  # noqa E501


def get_html(page: int, category: dict) -> Result[str, str]:
    logging.info(f"category={category['name']} page={page}")

    category_str = f"{category['id_category']}-{category['name']}"
    url = f"https://www.catawiki.com/en/c/{category_str}?page={page}"

    try:
        response = requests.get(url=url, headers=get_headers())
    except Exception:
        time.sleep(10)
        return Err(f"Unable to get page url={url}")

    if response.status_code != 200:
        return Err(
            f"unable to fetch data from {url}: status_code={response.status_code}"
        )

    return Ok(str(response.content.decode("utf-8")))


def get_json(category: dict, page: int, inputs: str) -> Result[dict, str]:
    logging.info(f"category={category['name']} page={page}")

    soup = BeautifulSoup(markup=inputs, features="html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__")
    if script_tag is None:
        return Err("unable to find script tag in the output")

    json_content = script_tag.string
    try:
        outputs = json.loads(json_content)
    except Exception as e:
        return Err(str(e))
    return Ok(outputs)


def get_db_connection(cache_path: str) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(database=os.path.join(cache_path, "data.duckdb"))
    return con


def init_tables(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(query=open("./sql/init_products.sql", mode="r").read())


def get_products(
    page: int,
    inputs: dict,
    category: dict,
    con: duckdb.DuckDBPyConnection,
) -> Result[str, str]:
    try:
        outputs = inputs["props"]["pageProps"]["categoryLots"]["lots"]
    except Exception:
        outputs = list()

    if len(outputs) == 0:
        return Err("no more products detected")

    existing_ids = set(
        con.execute(query="SELECT id FROM products").fetch_df()["id"].tolist()
    )

    outputs = [output for output in outputs if output is not None and output.get("id") not in existing_ids]

    logging.info(f"category={category['name']} page={page} #_products={len(outputs)}")
    for output in outputs:
        if output is None or output.get("id", None) is None:
            continue
        con.execute(
            query=open("./sql/set_product.sql", mode="r").read(),
            parameters=[
                category["id_category"],
                category["name"],
                output.get("id", None),
                output.get("title", None),
                output.get("subtitle", None),
                output.get("thumbImageUrl", None),
                output.get("originalImageUrl", None),
                output.get("favoriteCount", None),
                output.get("url", None),
                output.get("localized", None),
                output.get("translatedTitle", None),
                output.get("translatedSubtitle", None),
                output.get("auctionId", None),
                output.get("pubnubChannel", None),
                output.get("useRealtimeMessageFallback", None),
                output.get("isContentExplicit", None),
                output.get("reservePriceSet", None),
                output.get("biddingStartTime", None),
                output.get("buyNow", None),
                output.get("description", None),
                output.get("sellerId", None),
                output.get("sellerShopName", None),
                output.get("live", dict()).get("id", None),
                output.get("live", dict()).get("reservePriceMet", None),
                output.get("live", dict()).get("bid", dict()).get("EUR", None),
                output.get("live", dict()).get("bid", dict()).get("USD", None),
                output.get("live", dict()).get("bid", dict()).get("GBP", None),
                output.get("live", dict()).get("biddingEndTime", None),
                output.get("live", dict()).get("biddingStartTime", None),
                output.get("live", dict()).get("highestBidderToken", None),
                output.get("live", dict()).get("favoriteCount", None),
                output.get("live", dict()).get("winnerToken", None),
                output.get("live", dict()).get("closeStatus", None),
                output.get("live", dict()).get("isBuyNowAvailable", None),
            ],
        )
        existing_ids.add(output.get("id"))

    return Ok("process complemeted")


def get_nb_items(con: duckdb.DuckDBPyConnection, category: dict) -> int:
    return con.execute(query=f"""
    SELECT COUNT(*)
    FROM products
    WHERE id_category = {category["id_category"]}
    """).fetchall()[0][0]


def get_category_data(
    category: dict, con: duckdb.DuckDBPyConnection
) -> Result[str, str]:
    logging.info(f"processing category={category['name']}")

    page = 1
    nb_items = get_nb_items(con=con, category=category)
    if nb_items > 24 * 20:
        return Ok(f"category={category} status=alread_processed")
    elif nb_items > 0:
        page = int(nb_items / 24)

    while page <= 20:
        output_html = get_html(category=category, page=page)
        if is_err(output_html) is True:
            return Err(output_html.value)

        output_json = get_json(inputs=output_html.value, category=category, page=page)
        if is_err(output_json) is True:
            return Err(str(output_json.value))

        output_product = get_products(
            con=con,
            page=page,
            category=category,
            inputs=output_json.value,  # type: ignore
        )

        time.sleep(2)

        if is_err(output_product):
            break

        page = page + 1

    return Ok(f"category={category} status=done")


def get_data(cache_path: str) -> Result[str, str]:
    categories = list()

    con = get_db_connection(cache_path=cache_path)
    init_tables(con=con)

    categories_path = os.path.join(cache_path, "categories.jsonl")
    with open(categories_path, mode="r") as r:
        for row in r.readlines():
            categories.append(json.loads(row))

    for category in categories:
        output = get_category_data(
            con=con,
            category=category,
        )

        if is_err(output):
            logging.error(output.err_value)
            continue

    con.close()
    return Ok("scraping completed")
