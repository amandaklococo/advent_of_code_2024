###Find the difference between the nth smallest number in col1 and col2
###Sum these differences

import requests
import pandas as pd


url = "https://adventofcode.com/2024/day/1/input"

headers = {
    "Cookie": "session=53616c7465645f5fa76586551f9990d58d70aa5a44bbe86c34f2a12b09917e5bbeab654bb0fbda6b70be1644275b3b25f8936083e32b840d5f03b1db0d8cae21"
}

response = requests.get(url, headers=headers)

###Check if the request was successful
if response.status_code == 200:
    data = response.text.splitlines()
    data = [line.split() for line in data]

    df = pd.DataFrame(data, columns=["col1", "col2"])
    df = df.astype(int)
    
    ###Sort each column in ascending order
    df['col1'] = df['col1'].sort_values().values
    df['col2'] = df['col2'].sort_values().values
    
    df['diff'] = abs(df['col1'] - df['col2'])
    sum =  df['diff'].sum()
    print(sum)

    df['count'] = 0

    for row, value in enumerate(df['col1']):
        df.loc[row, 'count'] = (df['col2'] == value).sum() * value

    print(df['count'].sum())

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
