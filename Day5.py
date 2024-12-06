import pandas as pd

from fetch_data import fetch_data


def clean_data():
    data = fetch_data(day=5)
    data = data.splitlines()
    data = [line.split() for line in data]

    df = pd.DataFrame(data)

    df_rules = df[0:df.index[df.isnull().all(1)][0]]

    orders = df[df.index[df.isnull().all(1)][0]+1:]
    orders = orders[0].str.split(',', expand=True)
    orders = orders.values.tolist()

    new_list = []

    ###Remove nones
    for my_list in orders:
        my_list = list(filter(lambda item: item is not None, my_list))
        new_list.append(my_list)
    
    return new_list, df_rules

def find_incorrect_order(new_list, df_rules):
    ###Remove lists that do not fit the criteria
    for my_list in new_list:
        for element_number, element in enumerate(my_list):
            for repeat in my_list[element_number:]:
                if f'{repeat}|{element}' in df_rules[0].values:
                    new_list = [x for x in new_list if x != my_list]
                    break
                else:
                    pass
    
    return new_list

def find_middle(new_list):
    count = 0 

    ###Find middle of each list
    for my_list in new_list:
        middle = int((len(my_list)-1)/ 2)
        count = count + int(my_list[middle])

    return count
            

def get_rejected_lists(new_list, approved_lists, df_rules):
    
    ###Convert lists of lists to sets of tuples
    set1 = set(tuple(x) for x in new_list)
    set2 = set(tuple(x) for x in approved_lists)

    ###Find the differences
    difference = set1.symmetric_difference(set2)

    ###Convert back to lists of lists to find the rejected lists
    result = [list(x) for x in difference]

    rules_broken = 1
    new_order = []

    ###Run this loop until no rules are broken
    while rules_broken > 0:
        rules_broken = 0  
        new_order = []
        ###Swap list elements that violate the criteria
        for my_list in result:
            for element_number, element in enumerate(my_list):
                for repeat in my_list[element_number:]:
                    if f'{repeat}|{element}' in df_rules[0].values:
                        rules_broken += 1 
                        e, r = my_list.index(element), my_list.index(repeat)  
                        my_list[e], my_list[r] = my_list[r], my_list[e] 
                        break 

            new_order.append(my_list)

        print(f"Rules broken: {rules_broken}")
    
    return new_order


if __name__ == "__main__":
    new_list, df_rules = clean_data()
    approved_lists = find_incorrect_order(new_list=new_list, df_rules=df_rules)
    part1 = find_middle(new_list=approved_lists)
    print(f"Part 1 solution: {part1}")
    shuffle = get_rejected_lists(new_list=new_list, approved_lists=approved_lists, df_rules=df_rules)
    part2 = find_middle(new_list=shuffle)
    print(f"Part 2 solution: {part2}")