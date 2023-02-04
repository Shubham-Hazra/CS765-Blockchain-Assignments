
class Transaction:
    def __init__(self,txn_id, sender_id, receiver_id, amount, n): # The simulator ensures distinct transaction ids
        self.txn_id = txn_id
        self.id = f"Txn_{self.txn_id}"
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.message = f"{self.id}: {self.sender_id} pays {self.receiver_id} {self.amount} coins"
        self.received = [0] * n

    # Function for printing transaction information
    def print_transaction(self):
        print(self.message)

    # Function for getting transaction message
    def get_transaction(self):
        return self.message


# Testing
if __name__ == "__main__":
    txn1 = Transaction(0,1, 2, 3)
    txn2 = Transaction(1, 2, 3, 4)
    txn1.print_transaction()
    txn2.print_transaction()
