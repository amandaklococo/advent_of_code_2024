import pandas as pd

from fetch_data import fetch_data

data = fetch_data(day=4)

data = data.splitlines()
data = [line.split() for line in data]

df = pd.DataFrame(data)
df = df[0].apply(lambda x: pd.Series(list(x)))

count = 0
count_x_shape = 0 

for row in df.index:
    for col in df.columns:
        if df.loc[row][col] == 'X':
            
            ###Forwards >
            if (col != len(df.columns)-1) and (df.loc[row][col+1] == 'M'):
                if (col != len(df.columns)-2) and (df.loc[row][col+2] == 'A'):
                    if (col != len(df.columns)-3) and (df.loc[row][col+3] == 'S'):
                        count = count + 1

            ###Backwards <
            if (col != 0) and (df.loc[row][col-1] == 'M'):
                if (col != 1) and (df.loc[row][col-2] == 'A'):
                    if (col != 2) and (df.loc[row][col-3] == 'S'):
                        count = count + 1
            
            ###Up ^
            if (row != 0) and (df.loc[row-1][col] == 'M'):
                if (row != 1) and (df.loc[row-2][col] == 'A'):
                    if (row != 2) and (df.loc[row-3][col] == 'S'):
                        count = count + 1

            ###Down v
            if (row != len(df.index)-1) and (df.loc[row+1][col] == 'M'):
                if (row != len(df.index)-2) and (df.loc[row+2][col] == 'A'):
                    if (row != len(df.index)-3) and (df.loc[row+3][col] == 'S'):
                        count = count + 1

            ###Top left diagonal
            if (col != 0) and (row != 0) and (df.loc[row-1][col-1] == 'M'):
                if (col != 1) and (row != 1) and (df.loc[row-2][col-2] == 'A'):
                    if (col != 2) and (row != 2) and (df.loc[row-3][col-3] == 'S'):
                        count = count + 1

            ###Top right diagonal
            if (col != len(df.columns)-1) and (row != 0) and (df.loc[row-1][col+1] == 'M'):
                if (col != len(df.columns)-2) and (row != 1) and (df.loc[row-2][col+2] == 'A'):
                    if (col != len(df.columns)-3) and (row != 2) and (df.loc[row-3][col+3] == 'S'):
                        count = count + 1

            ###Bottom left diagonal
            if (col != 0) and (row != len(df.index)-1) and (df.loc[row+1][col-1] == 'M'):
                if (col != 1) and (row != len(df.index)-2) and (df.loc[row+2][col-2] == 'A'):
                    if (col != 2) and (row != len(df.index)-3) and (df.loc[row+3][col-3] == 'S'):
                        count = count + 1

            ###Bottom right diagonal
            if (col != len(df.columns)-1) and (row != len(df.index)-1) and (df.loc[row+1][col+1] == 'M'):
                if (col != len(df.columns)-2) and (row != len(df.index)-2) and (df.loc[row+2][col+2] == 'A'):
                    if (col != len(df.columns)-3) and (row != len(df.index)-3) and (df.loc[row+3][col+3] == 'S'):
                        count = count + 1
            
        ###M is in the top left of the X
        if (df.loc[row][col] == 'M') and (col < len(df.columns)-2) and (row < len(df.index)-2):
            if df.loc[row+1][col+1] == 'A':
                ###The other M is the top right of the X
                if (df.loc[row][col+2] == 'M') and (df.loc[row+2][col+2] == 'S') and (df.loc[row+2][col] == 'S'):
                    count_x_shape = count_x_shape + 1
                ###The other M is the bottom left of the X
                if (df.loc[row][col+2] == 'S') and (df.loc[row+2][col+2] == 'S') and (df.loc[row+2][col] == 'M'):
                    count_x_shape = count_x_shape + 1
        
        ###S is in the top left of the X
        if (df.loc[row][col] == 'S') and (col < len(df.columns)-2) and (row < len(df.index)-2):
            if df.loc[row+1][col+1] == 'A':
                ###The other S is the top right of the X
                if (df.loc[row][col+2] == 'S') and (df.loc[row+2][col+2] == 'M') and (df.loc[row+2][col] == 'M'):
                    count_x_shape = count_x_shape + 1
                ###The other S is the bottom left of the X
                if (df.loc[row][col+2] == 'M') and (df.loc[row+2][col+2] == 'M') and (df.loc[row+2][col] == 'S'):
                    count_x_shape = count_x_shape + 1

print(f"Part 1 solution: {count}")
print(f"Part 2 solution: {count_x_shape}")