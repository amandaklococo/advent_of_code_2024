import pandas as pd
import numpy as np
import multiprocessing as mp
from functools import partial
from itertools import product

from fetch_data import fetch_data

def clean_data():
    data = fetch_data(day=7)

    data = data.splitlines()
    data = [line.split() for line in data]

    df = pd.DataFrame(data)
    df[0] = df[0].str.replace(':', '')
    df = df.replace(np.nan, 0).astype(int).replace(0, np.nan)

    test_values = df[0].to_list()

    df = df.drop(columns=[0])

    list_of_lists = df.stack().groupby(level=0).apply(list).tolist()

    return test_values, list_of_lists

def evaluate_left_to_right(expression):
  elements = expression.split()
  result = int(elements[0])

  for i in range(1, len(elements), 2):
    operator = elements[i]
    number = int(elements[i + 1])

    if operator == '+':
      result += number

    elif operator == '*':
      result *= number

    elif operator == '||':
       result = int(f"{int(result)}{int(number)}")
    
    else:
      raise ValueError("Invalid operator: {}".format(operator))

  return result


def apply_operations(operations, test_values, list_of_lists, vals):
    
    sum_list = []

    val_to_match = test_values[list_of_lists.index(vals)]

    for ops in product(operations, repeat=len(vals) - 1):
        expression = str(int(vals[0]))
        
        for num, op in zip(vals[1:], ops):
            expression += ' ' + op + ' ' + str(int(num))

        result = evaluate_left_to_right(expression=expression)

        if result == val_to_match:
            sum_list.append(result)
            break

    return sum_list


if __name__ == "__main__":
    
    test_values, list_of_lists = clean_data()

    operations = ["+", "*"]

    with mp.Pool(processes=16) as p:
        results = p.map(partial(apply_operations, 
                                operations,
                                test_values,
                                list_of_lists),
                                [vals for vals in list_of_lists])
    results = list(np.concatenate(results))
    print(f"Part 1 solution: {int(sum(results))}")

    operations = ["+", "*", "||"]

    with mp.Pool(processes=16) as p:
        results = p.map(partial(apply_operations, 
                                operations,
                                test_values,
                                list_of_lists),
                                [vals for vals in list_of_lists])
    results = list(np.concatenate(results))
    print(f"Part 2 solution: {int(sum(results))}")
