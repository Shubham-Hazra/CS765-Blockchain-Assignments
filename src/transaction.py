import threading


class transaction:
    id = 0
    lock = threading.Lock()

    def __init__(self, sender_id, receiver_id, amount):
        transaction.lock.acquire()
        transaction.id += 1
        self.id = f"Txn_{transaction.id}"
        transaction.lock.release()
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.message = f"{self.id}: {self.sender_id} pays {self.receiver_id} {self.amount} coins"

    def print_transaction(self):
        print(self.message)

    def get_transaction(self):
        return self.message


# Testing
if __name__ == "__main__":
    txn1 = transaction(1, 2, 3)
    txn2 = transaction(2, 3, 4)
    txn1.print_transaction()
    txn2.print_transaction()
