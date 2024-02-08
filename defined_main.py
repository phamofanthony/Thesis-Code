import json
from collections import Counter
from defined_log_generator import generate_defined_data

def defined_results(num_data_items, num_transactions, min_ops_per_transaction, max_ops_per_transaction, num_training_data):
    #create training data
    generate_defined_data(file_name="defined_training_data", num_data_items=num_data_items, num_transactions=200000, min_ops_per_transaction=min_ops_per_transaction, max_ops_per_transaction=max_ops_per_transaction)
    
    #find common patterns
    patterns = find_defined_patterns(min_sequence_length=3, min_num_occurences=2)

    #generate test data
    generate_defined_data(file_name="defined_testing_data", num_data_items=num_data_items, num_transactions=num_transactions, min_ops_per_transaction=min_ops_per_transaction, max_ops_per_transaction=max_ops_per_transaction)

    #analyze test data
    return analyze_defined_test_data(patterns = patterns, num_transactions = num_transactions, file_name = 'defined_testing_data.json')




def find_defined_patterns(min_sequence_length, min_num_occurences):
    with open('defined_training_data.json', 'r') as json_file:
        data = json.load(json_file)
    ops_arrays = [entry['ops'] for entry in data]
    all_ops = [op for ops_array in ops_arrays for op in ops_array]
    sequences = [tuple(all_ops[i:i+min_sequence_length]) for i in range(len(all_ops)-(min_sequence_length-1))] #Find sequences of length 3 or longer
    sequence_counts = Counter(sequences) #Count the occurrences of each sequence
    filtered_sequences = {seq: count for seq, count in sequence_counts.items() if count >= min_num_occurences} #Filter sequences that occur in 5 or more arrays
    filtered_sequences_arrays = [list(seq) for seq, count in filtered_sequences.items()]
    """ print("Sequences of length 3 or longer that occur in 3 or more arrays:")
    for seq, count in filtered_sequences.items():
        print(f"Sequence: {seq}, Occurrences: {count}")  """
    return filtered_sequences_arrays

def analyze_defined_test_data(patterns, num_transactions, file_name):
    patterns = patterns
    intermediate_patterns = []
    with open(file_name, 'r') as json_file:
        objects = json.load(json_file)
    intermediate_patterns = []
    ops_arrays = [obj['ops'] for obj in objects]
    good_nonflagged = 0
    bad_nonflagged = 0

    for i in range(num_transactions): #For each transaction: 
        for pattern in patterns: #Check every single pattern
            if i < round(0.95 * num_transactions): #If it's a good transaction
                if is_subsequence(pattern, ops_arrays[i]): #And pattern matches:
                    good_nonflagged += 1 #Don't flag
                    #print(f"{pattern} is a subsequence of {ops_arrays[i]}")
                    break
            else: #If it's a bad transaction
                if is_subsequence(pattern, ops_arrays[i]): #And pattern matches:
                    bad_nonflagged += 1 #Don't flag
                    #print(f"{pattern} is a subsequence of {ops_arrays[i]}")
                    break
        
        if i <= round(0.95 * num_transactions):
            update_intermediate_patterns(ops_arrays[i], intermediate_patterns, patterns)
    
    #print(f"{num_transactions} total transactions, {good_nonflagged} good-nonflagged. {bad_nonflagged} bad-nonflagged")
    #print("Defined Results")
    #print(f"    Good Transactions: {good_nonflagged}/{round(0.95 * num_transactions)} passed, {round(0.95 * num_transactions)-good_nonflagged}/{round(0.95 * num_transactions)} were flagged as suspicious")
    #print(f"    Bad Transactions: {bad_nonflagged}/{num_transactions - round(0.95 * num_transactions)} passed, {num_transactions - round(0.95 * num_transactions) - bad_nonflagged}/{num_transactions - round(0.95 * num_transactions)} were flagged as suspicious")
    #print(f"    Summary: {num_transactions - good_nonflagged - bad_nonflagged} transactions were blocked, where only {num_transactions - round(0.95 * num_transactions)} should have been")

    good_flagged = round(0.95 * num_transactions)-good_nonflagged
    bad_flagged = num_transactions - round(0.95 * num_transactions) - bad_nonflagged
    return good_nonflagged, good_flagged, bad_nonflagged, bad_flagged



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
