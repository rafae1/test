from collections import defaultdict

import requests

"""
    In this challenge, use the HTTP GET method to retrieve information from a 
    database of Card Transactions records for users.
    Query https://jsonmock.hackerrank.com/api/transactions/search?txnType=txn 
    where txn is the transaction type of the record passed to the function. 
    This will return all records that have the given transaction type. The query
    response is paginated and can be futher accessed by appending to the 
    query string &page=num where num is the number.

    The query response from the API is a JSON response.

    Given the location id (locationId) and the provided transaction type 
    (txnType) return 2d array containing the total amount transacted by each 
    user at the given locationId.

    The array will be in the format [[1, 1200], [2, 2333]] where the item at 
    index 0 in the inner array denotes the id of the user and item at index 1 
    denotes the total amount transacted (either debit or credit based on input
    txnType). The items in the outer array should be sorted by the ids of 
    the user. Note that the search is not case sensitive. If no records are
    found matching the filter criteria, it should return [[-1, -1]] 
"""


def get_txn_amount_by_loc(location_id: int, txn_type: str) -> list:
    base_url = "https://jsonmock.hackerrank.com/api/transactions/search"
    user_amount = defaultdict(float)
    page, total_pages = 1, 1
    while page <= total_pages:
        params = {"page": page, "txnType": txn_type}
        json_data = requests.get(base_url, params=params).json()
        total_pages = json_data["total_pages"]
        for d in json_data['data']:
            if d['location']['id'] == location_id:
                amount = float(d['amount'][1:].replace(',', ''))
                user_amount[d['userId']] += amount
        page += 1

    return sorted([k, round(v, 2)] for k, v in user_amount.items()) \
        if user_amount else [[-1, -1]]


if __name__ == '__main__':
    for loc in range(10):
        print(f"Location: {loc}")
        print(f"Debit response: {get_txn_amount_by_loc(loc, 'debit')}")
        print(f"Credit response: {get_txn_amount_by_loc(loc, 'credit')}\n")
