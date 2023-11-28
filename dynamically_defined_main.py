import json
from collections import Counter
from dynamic_log_generator import *

def main():
    #create training data / list of patterns
    patterns = generate_patterns(num_data_items=8, num_transactions=5)

    #generate test data
    generate_testing_data("dynamic_testing_data", num_data_items=8, num_transactions=100, patterns_list=patterns)

    #analyze test data
    analyze_test_data(patterns = patterns, num_transactions = 100)


def analyze_test_data(patterns, num_transactions):
    patterns = patterns
    with open('dynamic_testing_data.json', 'r') as json_file:
        objects = json.load(json_file)
    intermediate_patterns = []
    ops_arrays = [obj['ops'] for obj in objects]
    good_nonflagged = 0
    bad_nonflagged = 0

    for i in range(num_transactions):
        for pattern in patterns:
            if i <= round(0.95 * num_transactions):
                if is_subsequence(pattern, ops_arrays[i]):
                    good_nonflagged += 1
                    #print(f"{pattern} is a subsequence of {ops_arrays[i]}")
                    break
            else:
                if is_subsequence(pattern, ops_arrays[i]):
                    bad_nonflagged += 1
                    #print(f"{pattern} is a subsequence of {ops_arrays[i]}")
                    break
        
        if i <= round(0.95 * num_transactions):
            update_intermediate_patterns(ops_arrays[i], intermediate_patterns, patterns)
    
    #print(f"{num_transactions} total transactions, {good_nonflagged} good-nonflagged. {bad_nonflagged} bad-nonflagged")
    print(f"Good Transactions: {good_nonflagged}/{round(0.95 * num_transactions)} passed, {round(0.95 * num_transactions)-good_nonflagged}/{round(0.95 * num_transactions)} were flagged as suspicious")
    print(f"Bad Transactions: {bad_nonflagged}/{num_transactions - round(0.95 * num_transactions)} passed, {num_transactions - round(0.95 * num_transactions) - bad_nonflagged}/{num_transactions - round(0.95 * num_transactions)} were flagged as suspicious")
    print(f"Summary: {num_transactions - good_nonflagged - bad_nonflagged} transactions were blocked, where only {num_transactions - round(0.95 * num_transactions)} should have been")



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

def update_intermediate_patterns(new_sequence, intermediate_patterns, patterns):
    intermediate_patterns.append(new_sequence)
    sequence_count = {}
    
    # Count occurrences of sequences in arrays
    for array in intermediate_patterns:
        for i in range(len(array) - 2):  # Check sequences of length 3 or longer
            sequence = tuple(array[i:i+3])
            sequence_count[sequence] = sequence_count.get(sequence, 0) + 1

    # Filter sequences with count >= 5
    common_sequences = [sequence for sequence, count in sequence_count.items() if count >= 5]

    # If patterns doesn't already contain the common sequences, add it to patterns
    for sequence in common_sequences:
        if sequence not in patterns:
            patterns.append(sequence)

main()



