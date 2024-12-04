import pandas as pd
from fetch_data import fetch_data

data = fetch_data(day=1)

data = data.splitlines()
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