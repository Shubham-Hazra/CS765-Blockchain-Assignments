import threading


# Class for transaction
class Transaction:
    id = 0  # Global transaction id
    lock = threading.Lock()  # Lock for transaction id

    def __init__(self, sender_id, receiver_id, amount):
        transaction.lock.acquire()  # Acquire lock
        transaction.id += 1  # Increment global transaction id
        self.id = f"Txn_{transaction.id}"
        transaction.lock.release()  # Release lock
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.message = f"{self.id}: {self.sender_id} pays {self.receiver_id} {self.amount} coins"

    # Function for printing transaction information
    def print_transaction(self):
        print(self.message)

    # Function for getting transaction message
    def get_transaction(self):
        return self.message


# Testing
if __name__ == "__main__":
    txn1 = transaction(1, 2, 3)
    txn2 = transaction(2, 3, 4)
    txn1.print_transaction()
    txn2.print_transaction()
