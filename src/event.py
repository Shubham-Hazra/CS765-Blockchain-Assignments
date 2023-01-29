import threading
import time


class Event:
    def __init__(self, sender, message, is_block):
        self.sender = sender
        self.is_block = is_block
        self.message = message
        self.time = time.time()

    def print(self):
        print("Event from " + str(self.sender) + " at time " +
              str(self.time) + " with message " + str(self.message))

    def send(self, receiver_function, sleep_time):
        def send_message():
            time.sleep(sleep_time)
            receiver_function(self)
        t = threading.Thread(target=send_message)
        t.start()


# Testing
msg = Event(1, "Hello", False)
msg.print()
msg.send(print, 2)
