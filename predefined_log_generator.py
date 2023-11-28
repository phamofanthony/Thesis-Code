import random
import json
import copy
import math

class Transaction:
    def __init__(self, id, ops):
        self.id = id
        self.ops = ops

    def output_transaction(self):
        return "{Transaction ID: " + str(self.id) + ", Operations: " + str(self.ops) + "}"

def operation_string(op, data_item):
    return op + "[" + str(data_item) + "]"

def generate_patterns(num_data_items, num_transactions):
    #sequence generation variables
    data_items = range(num_data_items)
    operations = ["R", "W"]
    transactions = []

    #pattern generation variables
    patterns = []
    num_patterns = num_transactions
    min_ops_per_pattern = 3
    max_ops_per_pattern = 4

    #generate random patterns
    for i in range(num_patterns):
        num_operations = random.randrange(min_ops_per_pattern, max_ops_per_pattern + 1)
        current_pattern = []
        current_read_operations = []
        current_write_operations = []
        
        for operation in range(num_operations):
            new_operation = operation_string(random.choice(operations), random.choice(data_items))
            while ((current_read_operations.count(new_operation) != 0) or (current_write_operations.count(new_operation) != 0) or ((new_operation[0] == "R") and (current_write_operations.count("W[" + str(new_operation[2]) + "]") != 0))):
                new_operation = operation_string(random.choice(operations), random.choice(data_items))
            current_pattern.append(new_operation)
            if new_operation[0] == "R":
                current_read_operations.append(new_operation)
            elif new_operation[0] == "W":
                current_write_operations.append(new_operation)
        patterns.append(current_pattern)

    return patterns

def generate_testing_data(file_name, num_data_items, num_transactions, patterns_list):
    min_ops_per_transaction = 3
    max_ops_per_transaction = 5
    data_items = range(num_data_items)
    operations = ["R", "W"]
    transactions = []
    GoodPatterned = 0
    GoodRandomized = 0
    Bad = 0

    for i in range(num_transactions):
        transaction_id = i + 1
        num_operations = random.randrange(min_ops_per_transaction, max_ops_per_transaction + 1)
        if i < round(0.95 * num_transactions):
            if random.random() < 0.95:
                transactions.append(create_transaction("patterned", transaction_id, operations, data_items, num_operations, patterns_list))
                GoodPatterned += 1
            else:
                transactions.append(create_transaction("randomized", transaction_id, operations, data_items, num_operations, patterns_list))
                GoodRandomized += 1
        else:
            transactions.append(create_transaction("randomized", transaction_id, operations, data_items, num_operations, patterns_list))
            Bad += 1

    #print(f"There are {GoodPatterned} good patterned transactions, {GoodRandomized} good randomized transactions, and {Bad} bad randomized transactions")
    transactions_dict = [{"id": t.id, "ops": t.ops} for t in transactions]
    with open(file_name + ".json", 'w') as json_file:
        json.dump(transactions_dict, json_file, indent=2)


def create_transaction(type, transaction_id, operations, data_items, num_operations, patterns_list):
    patterns = copy.deepcopy(patterns_list)
    if type == "patterned":
        current_operations = random.choice(patterns)
        current_operations.append("C" + str(transaction_id))
        return Transaction(transaction_id, current_operations)
    elif type == "randomized":
        current_operations = []
        current_read_operations = []
        current_write_operations = []
        for operation in range(num_operations):
            new_operation = operation_string(random.choice(operations), random.choice(data_items))
            while ((current_read_operations.count(new_operation) != 0) or (current_write_operations.count(new_operation) != 0) or ((new_operation[0] == "R") and (current_write_operations.count("W[" + str(new_operation[2]) + "]") != 0))):
                new_operation = operation_string(random.choice(operations), random.choice(data_items))
            current_operations.append(new_operation)
            if new_operation[0] == "R":
                current_read_operations.append(new_operation)
            elif new_operation[0] == "W":
                current_write_operations.append(new_operation)
        current_operations.append("C" + str(transaction_id))
        return Transaction(transaction_id, current_operations)
