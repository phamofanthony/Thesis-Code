def find_repeated_sequences_combined(file_path):
    def find_repeated_sequences(transactions):
        sequence_count = {}
        
        # Iterate through each transaction
        for transaction in transactions:
            operations = transaction['Operations']
            
            # Iterate through each operation in the transaction
            for i in range(len(operations) - 2):
                sequence = tuple(operations[i:i + 3])  # Get a sequence of three operations
                
                # Check if the sequence has occurred before
                if sequence in sequence_count:
                    sequence_count[sequence] += 1
                else:
                    sequence_count[sequence] = 1
        
        # Filter sequences that occurred at least 3 times
        repeated_sequences = {k: v for k, v in sequence_count.items() if v >= 3}
        
        return repeated_sequences

    with open(file_path, 'r') as file:
        transactions = []
        for line in file:
            # Assuming each line is a dictionary representation of a transaction
            transaction = eval(line.strip())
            transactions.append(transaction)

    repeated_sequences = find_repeated_sequences(transactions)
    return repeated_sequences

# Example usage
file_path = "training_data.txt"
repeated_sequences = find_repeated_sequences_combined(file_path)
print("Repeated Sequences:")
for sequence, count in repeated_sequences.items():
    print(f"{sequence}: {count} times")