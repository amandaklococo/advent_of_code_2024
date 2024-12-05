import pandas as pd
import numpy as np

from fetch_data import fetch_data

def data_cleaning():
    data = fetch_data(day=2)

    data = data.splitlines()
    data = [line.split() for line in data]

    df = pd.DataFrame(data)
    df = df.replace(np.nan, 0).astype(int).replace(0, np.nan)

    return df

def find_true_rows(df):
    ###Calculate the difference between consecutive elements in each row
    df_diff = df.diff(axis=1)

    ###Find increasing rows that meet the conditions
    monotone_incr_rows = df_diff.replace(np.nan, 1).gt(0).all(skipna=True, axis=1)
    diff_less_than_3 = df_diff.replace(np.nan, 1).le(3).all(skipna=True, axis=1)
    df_incr = pd.concat([monotone_incr_rows, diff_less_than_3], axis=1)
    df['increasing_rows'] = df_incr.apply(lambda x: 1 if x[0] == True & x[1] == True else 0, axis=1)

    ###Find decreasing rows that meet the condtions
    df_diff = -1 * df_diff
    monotone_decr_rows = df_diff.replace(np.nan, 1).gt(0).all(skipna=True, axis=1)
    diff_less_than_3 = df_diff.replace(np.nan, 1).le(3).all(skipna=True, axis=1)
    df_decr = pd.concat([monotone_decr_rows, diff_less_than_3], axis=1)
    df['decreasing_rows'] = df_decr.apply(lambda x: 1 if x[0] == True & x[1] == True else 0, axis=1)

    return df

def drop_cols(df):
    df_drop = df.copy()
    df_drop = df_drop.drop(columns=['increasing_rows', 'decreasing_rows'], axis=1)

    for column in df_drop.columns:
        df_temp = df_drop.copy()
        df_temp = df_temp.drop(columns=[column])
        df_temp = find_true_rows(df=df_temp)
        df['increasing_rows'] = df['increasing_rows'] + df_temp['increasing_rows']
        df['decreasing_rows'] = df['decreasing_rows'] + df_temp['decreasing_rows']
    
    df['increasing_rows'] = np.where(df['increasing_rows'] > 0, 1, 0)
    df['decreasing_rows'] = np.where(df['decreasing_rows'] > 0, 1, 0)

    return df
        

if __name__ == "__main__":
    df = data_cleaning()
    df = find_true_rows(df=df)
    print(f"Part 1 solution: {df['increasing_rows'].sum() + df['decreasing_rows'].sum()}")
    df = drop_cols(df=df)
    print(f"Part 2 solution: {df['increasing_rows'].sum() + df['decreasing_rows'].sum()}")