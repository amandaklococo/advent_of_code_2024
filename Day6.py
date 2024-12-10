import pandas as pd 
import numpy as np
import multiprocessing as mp
from functools import partial

from fetch_data import fetch_data

def clean_data():
    data = fetch_data(day=6)

    start_config = '^'

    data = data.splitlines()
    data = [line.split() for line in data]

    df = pd.DataFrame(data)
    df = df[0].apply(lambda x: pd.Series(list(x)))

    index, column = np.where(df == start_config)
    index = index[0]
    column = column[0]

    return df, index, column

def move_up(df, index, column, break_counter):
    while True:
        if df.loc[index-1, column] == '#':
            break
        
        index = index - 1
        df.loc[index, column] = 'X'

        if index - 1 == -1:
            break_counter = + 1
            break

    return df, index, column, break_counter

def move_right(df, index, column, break_counter):
    while True:
        if df.loc[index, column+1] == '#':
            break
        
        column = column + 1
        df.loc[index, column] = 'X'

        if column + 1 == len(df.columns + 1):
            break_counter = + 1
            break

    return df, index, column, break_counter

def move_down(df, index, column, break_counter):
    while True:
        if df.loc[index+1, column] == '#':
            break
        
        index = index + 1
        df.loc[index, column] = 'X'

        if index+1 == len(df.index+1):
            break_counter = + 1
            break

    
    return df, index, column, break_counter

def move_left(df, index, column, break_counter):
    while True:
        if df.loc[index, column-1] == '#':
            break
        
        column = column - 1
        df.loc[index, column] = 'X'
    
        if column-1 == -1:
            break_counter = 1
            break

    return df, index, column, break_counter

def grid_move(df, index, column, break_counter=0):
    
    while True:

        df, index, column, break_counter = move_up(df=df, index=index, column=column, break_counter=break_counter)
        if break_counter == 1:
            break

        df, index, column, break_counter = move_right(df=df, index=index, column=column, break_counter=break_counter)
        if break_counter == 1:
            break

        df, index, column, break_counter = move_down(df=df, index=index, column=column, break_counter=break_counter)
        if break_counter == 1:
            break
        
        df, index, column, break_counter = move_left(df=df, index=index, column=column, break_counter=break_counter)
        if break_counter == 1:
            break

    return df

def create_obstruction(args, break_counter=0):
    
    row, col, df, index, column = args
    breakers = 0

    df_loop = df.copy()
    df_loop.loc[row, col] = '#'
    
    index, column = np.where(df == '^')
    index = index[0]
    column = column[0]

    rotation_checks = 0
    running_total = []
    break_counter = 0

    while True:

        df_loop, index, column, break_counter = move_up(df=df_loop, index=index, column=column, break_counter=break_counter)
        total = df_loop.eq('X').values.sum()

        running_total.append(int(total))

        if break_counter == 1:
            break

        if (len(running_total) > 1) and (running_total[-1] == running_total[-2]):
            rotation_checks = rotation_checks + 1
        if rotation_checks == 8:
            breakers = breakers +  1
            break

        df_loop, index, column, break_counter = move_right(df=df_loop, index=index, column=column, break_counter=break_counter)
        if break_counter == 1:
            break                

        df_loop, index, column, break_counter = move_down(df=df_loop, index=index, column=column, break_counter=break_counter)
        if break_counter == 1:
            break

        df_loop, index, column, break_counter = move_left(df=df_loop, index=index, column=column, break_counter=break_counter)      
        if break_counter == 1:
            break

    return breakers

def call_multiprocess(df, index, column):

    args_list = [(row, col, df, index, column) for row in df.index for col in df.columns]

    with mp.Pool(processes=16) as p:
        results = p.map(create_obstruction, args_list)

    return results

if __name__ == "__main__":
    df, index, column = clean_data()
    df_move = grid_move(df=df, index=index, column=column)
    df_move = df_move.replace('^', 'X')
    position_counts = df_move.eq('X').values.sum()
    print(f"Part 1 solution: {position_counts}")
    
    df, index, column = clean_data()
    df_loop = call_multiprocess(df=df, index=index, column=column)
    print(f"Part 2 solution: {sum(df_loop)}")