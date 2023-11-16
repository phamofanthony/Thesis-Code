import json
from collections import Counter
from loggenerator import *

def main():
    #create training data / list of patterns
    patterns = generate_patterns(num_data_items=8, num_transactions=5)

    #generate test data
    generate_testing_data("testing_data", num_data_items=8, num_transactions=100, patterns_list=patterns)

    #analyze test data
    analyze_test_data(patterns)


def analyze_test_data(patterns):
    with open('testing_data.json', 'r') as json_file:
        objects = json.load(json_file)
    
    ops_arrays = [obj['ops'] for obj in objects]
    good_nonflagged = 0
    bad_nonflagged = 0

    for i in range(100):
        for pattern in patterns:
            if i <= 95:
                if is_subsequence(pattern, ops_arrays[i]):
                    good_nonflagged += 1
                    #print(f"{pattern} is a subsequence of {ops_arrays[i]}")
                    break
            else:
                if is_subsequence(pattern, ops_arrays[i]):
                    bad_nonflagged += 1
                    #print(f"{pattern} is a subsequence of {ops_arrays[i]}")
                    break
    
    print(f"Good Transactions: {good_nonflagged}/95 passed, {95-good_nonflagged}/95 were flagged as suspicious")
    print(f"Bad Transactions: {bad_nonflagged}/5 passed, {5-bad_nonflagged}/5 were flagged as suspicious")
    print(f"Summary: {100 - good_nonflagged - bad_nonflagged} transactions were blocked, where only {5 - bad_nonflagged} should have been")



def is_subsequence(list_a, list_b):
    # Initialize indices for both lists
    index_a = 0
    index_b = 0

    # Iterate through both lists
    while index_a < len(list_a) and index_b < len(list_b):
        # If the current elements match, move to the next element in List A
        if list_a[index_a] == list_b[index_b]:
            index_a += 1
        # Move to the next element in List B
        index_b += 1

    # If all elements of List A are found in List B in the same order, return True
    return index_a == len(list_a)

main()
