"""
Maksym Bilyk -- All __modules reserved__
"""
import pandas as pd
from config import country_file, complete_file

STARTING = "Preparing data......."

def loading_begin():
    """
    Returns
    -------
    set()
    set()
    set()
    dict()
    """
    print(STARTING + "\n" + "=" * len(STARTING))
    dota = pd.read_csv(country_file, encoding="utf-8", na_filter=False)
    code_dct__ = dict(zip(dota["Name"], dota["Code"]))
    data = pd.read_csv(complete_file)
    city_set__ = set(data["CITY"])
    country_set__ = set(data["COUNTRY"])
    data_base__ = dict(zip(zip(data["CITY"], data["COUNTRY"]), data["COORDS"]))
    return code_dct__, city_set__, country_set__, data_base__


code_dct, city_set, country_set, data_base = loading_begin()
