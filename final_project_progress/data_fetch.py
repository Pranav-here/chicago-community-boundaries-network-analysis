import os
import time
import requests
import pandas as pd

STATE = "17"
COUNTY = "031"
API_KEY = os.getenv("CENSUS_API_KEY", "")
ACS2022 = "https://api.census.gov/data/2022/acs/acs5"

CAS = {
    "15": "Portage Park",
    "25": "Austin",
    "53": "West Pullman",
    "62": "West Elsdon"
}

VARIABLES = {
    "B01003_001E": "total_pop",
    "B02001_002E": "white_alone",
    "B02001_003E": "black_alone",
    "B03003_003E": "hispanic",
    "B15003_001E": "edu_total",
    "B15003_022E": "ba_degree",
    "B15003_023E": "masters",
    "B15003_024E": "professional",
    "B15003_025E": "doctorate",
    "B25003_001E": "tenure_total",
    "B25003_003E": "renter_occupied",
    "B19013_001E": "median_hh_income",
    "B25064_001E": "median_gross_rent",
    "B05002_013E": "foreign_born",
    "B25002_001E": "housing_units_total",
    "B25002_003E": "vacant_units",
    "B25003_002E": "owner_occupied",
    "B08301_001E": "commute_total",
    "B08301_019E": "walk_to_work",
}

def get_ca_tracts(ca_id):
    ca_tracts = {
        "15": ["800100", "800200", "800300", "800400", "800500"],
        "25": ["250100", "250200", "250300", "250400", "250500"],
        "53": ["530100", "530200", "530300"],
        "62": ["620100", "620200", "620300", "620400"]
    }
    return ca_tracts.get(ca_id, [])

def census_api_get(url, params):
    if API_KEY:
        params["key"] = API_KEY
    for _ in range(3):
        try:
            resp = requests.get(url, params=params, timeout=90)
            if resp.status_code == 200:
                return resp.json()
            time.sleep(1.0)
        except:
            time.sleep(1.0)
    return None

def fetch_ca_blockgroups(ca_id, tract_list):
    var_list = list(VARIABLES.keys())
    records = []

    for tract in tract_list:
        params = {
            "get": ",".join(var_list + ["NAME"]),
            "for": "block group:*",
            "in": f"state:{STATE} county:{COUNTY} tract:{tract}"
        }
        data = census_api_get(ACS2022, params)
        if not data:
            continue

        header, *rows = data
        for row in rows:
            record = dict(zip(header, row))
            record["ca_id"] = ca_id
            record["ca_name"] = CAS[ca_id]
            record["geoid_bg"] = f"{record['state']}{record['county']}{record['tract']}{record['block group']}"
            records.append(record)
        time.sleep(0.3)

    return pd.DataFrame(records)

def fetch_all_cas():
    all_dfs = []

    for ca_id, ca_name in CAS.items():
        print(f"  Processing CA {ca_id} ({ca_name})...")
        tracts = get_ca_tracts(ca_id)
        if tracts:
            df_ca = fetch_ca_blockgroups(ca_id, tracts)
            if not df_ca.empty:
                all_dfs.append(df_ca)
                print(f"    Got {len(df_ca)} block groups")

    if not all_dfs:
        return None

    return pd.concat(all_dfs, ignore_index=True)
