"""
This script should run daily to:
    pull new data from Socrata
"""
import datetime as dt
import json
import os
from pprint import pprint

from flask import current_app

import requests

from inspectors.extensions import db
from inspectors.app import create_app
from inspectors.inspections.serializers import (
            SOCRATA_DATE_FMT,
            supervisor_schema,
            inspector_schema,
            inspection_schema,
            DataLoader
        )


USE_JSON_CACHE = False
json_cache_path = "data.json"


def json_cache_exists():
    return os.path.exists(json_cache_path)


def socrata_query():
    timedelta = dt.timedelta(days=-3)
    now = dt.datetime.now()
    three_days_ago = now + timedelta
    date_format = SOCRATA_DATE_FMT
    endpoint = "https://opendata.miamidade.gov/resource/ba6h-bksp.json"
    query = "?$where=date > '{three_days_ago}' AND date < '{now}'".format(
            three_days_ago=three_days_ago.strftime(date_format),
            now=now.strftime(date_format),
            )
    request = requests.get( endpoint + query )
    return request.json()


def get_data():
    if USE_JSON_CACHE:
        if json_cache_exists():
            with open(json_cache_path, 'r') as f:
                data = json.load(f)
        else:
            data = socrata_query()
            with open(json_cache_path, 'w') as f:
                json.dump(data, f)
    else:
        data = socrata_query()

    return data



def load_data():
    data = get_data()

    loaders = [DataLoader(s) for s in (
            supervisor_schema,
            inspector_schema,
            inspection_schema,
        )]

    for row in data:
        for loader in loaders:
            loader.slice_and_add(row)

    for loader in loaders:
        models = loader.save_models_or_report_errors()


def run():
    app = create_app()
    with app.app_context():
        load_data()

if __name__ == '__main__':
    run()

