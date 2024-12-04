###Find the difference between the nth smallest number in col1 and col2
###Sum these differences


import pandas as pd
from fetch_data import fetch_data

response = fetch_data(day=1)

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
    print(f"Sum for part 1: {df['diff'].sum()}")

    df['count'] = 0

    ###These lines do part 2
    for row, value in enumerate(df['col1']):
        df.loc[row, 'count'] = (df['col2'] == value).sum() * value

    print(f"Sum for part 2: {df['count'].sum()}")

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
