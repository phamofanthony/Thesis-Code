import random
import json

class Transaction:
    def __init__(self, id, ops):
        self.id = id
        self.ops = ops

    def output_transaction(self):
        return "{Transaction ID: " + str(self.id) + ", Operations: " + str(self.ops) + "}"

def operation_string(op, data_item):
    return op + "[" + str(data_item) + "]"

def generate_data(file_name, num_data_items, num_transactions):
    min_ops_per_transaction = 2
    max_ops_per_transaction = 5
    data_items = range(num_data_items)
    operations = ["R", "W"]
    transactions = []

    for i in range(num_transactions):
        transaction_id = i + 1
        num_operations = random.randrange(min_ops_per_transaction, max_ops_per_transaction + 1)
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
        transactions.append(Transaction(transaction_id, current_operations))

    transactions_dict = [{"id": t.id, "ops": t.ops} for t in transactions]
    with open(file_name + ".json", 'w') as json_file:
        json.dump(transactions_dict, json_file, indent=2)

