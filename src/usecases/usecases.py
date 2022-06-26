from loguru import logger

import requests
import json


def requests_funs(name, rq_type, url, params=None, json=None):
    """ rq_type = \"get\" or \"post\"
    return:
    1. 200 -> requests.get(post)
    2. 404 -> ""
    3. else-> None
    """
    if rq_type == "get":
        response = requests.get(url, params=params)
    elif rq_type == "post":
        response = requests.post(url, params=params, json=json)

    status_code = response.status_code

    if status_code == 200:
        logger.debug(f"{status_code} -> {name}")
        return response
    elif status_code == 404:
        logger.debug(f"{status_code} -> {name}")
        return ""
    else:
        logger.error(logger.debug(f"{status_code} -> {name}"))
        return None


def print_response_json(response):
    print(json.dumps(response, indent=2, ensure_ascii=False))


def write_response_json(response, path):
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(response, fp, indent=2, ensure_ascii=False)
