from loguru import logger

import requests
import json


def requests_funs(name, rq_type, url, params=None, json=None):
    """ request with parameter

    Inputs:
    rq_type = 'get' or 'post'

    Returns:
    resquests.get or resquests.post
    """

    if rq_type == "get":
        response = requests.get(url, params=params)
    elif rq_type == "post":
        response = requests.post(url, params=params, json=json)

    status_code = response.status_code

    if status_code == 200:
        logger.debug(f"{status_code} -> {name}")
    elif status_code == 404:
        logger.debug(f"{status_code} -> {name}")
    else:
        logger.error(logger.debug(f"{status_code} -> {name}"))
    return response


def print_response_json(response):
    print(json.dumps(response, indent=2, ensure_ascii=False))


def write_response_json(response, path):
    """ write dict or list to json file"""
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(response, fp, indent=2, ensure_ascii=False)
