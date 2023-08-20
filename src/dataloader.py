from sec_api import QueryApi
import pandas as pd
import sys

def get_13f_filings(start=0):
    print(f"Getting next 13F batch starting at {start}")
    
    query = {
      "query": { "query_string": { 
          "query": "formType:\"13F-HR\" AND NOT formType:\"13F-HR/A\" AND periodOfReport:\"2021-06-30\"" 
        } },
      "from": start,
      "size": "10",
      "sort": [{ "filedAt": { "order": "desc" } }]
    }

    response = queryApi.get_filings(query)

    return response['filings']


if __name__ == "__main__":

    queryApi = QueryApi(api_key="4ccc1c486d3ba64400cd76ebb2eaaa8fb6e0d597792cc83f7341abc288137fd9")
    print(queryApi)

    # fetch the 10 most recent 13F filings
    filings_batch = get_13f_filings(10)

    # load all holdings of the first 13F filing into a pandas dataframe 
    holdings_example = pd.json_normalize(filings_batch[0]['holdings'])

    print(holdings_example)