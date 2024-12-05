import re

from fetch_data import fetch_data

data = fetch_data(day=3)

def find_mul(data):
    regex = r"mul\((\d+),(\d+)\)"
    matches = re.findall(regex, data)
    matches = [(int(x[0]), int(x[1])) for x in matches]

    for entry in range(0, len(matches)):
        matches[entry] = matches[entry][0] * matches[entry][1]

    return matches

def do_and_dont(data):
    data = data.replace("\n", "")
    remove_dont = re.sub(r"don't\(\).*?do\(\)", "", data)
    new_matches = find_mul(data=remove_dont)

    return new_matches

if __name__ == "__main__":
    matches = find_mul(data=data)
    print(f"Part 1 solution: {sum(matches)}")
    new_matches = do_and_dont(data=data)
    print(f"Part 2 solution: {sum(new_matches)}")