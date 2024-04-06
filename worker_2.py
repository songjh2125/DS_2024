from queue_.listQueue import ListQueue
import threading
import time

class Producer:
    def __init__(self, items):
        self.__alive = True
        self.items = items
        self.pos = 0
        self.queue_ = ListQueue()
        self.worker = threading.Thread(target=self.run)

    def get_item(self):
        if self.pos < len(self.items):
            item = self.items[self.pos]
            self.pos += 1
            return item
        else:
            return None
    
    def run(self):
        while True:
            time.sleep(0.2)
            if self.__alive:
                item = self.get_item()
                if item:
                    self.queue_.enqueue(item) # Producer의 queue_에 도착한 순서대로 enqueue
                    print("Arrived:", item)
            else:
                break
        
        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()


class Consumer:
    def __init__(self):
        self.__alive = True
        self.queue_ = producer.queue_ # Producer(names)의 queue_를 이용
        self.worker = threading.Thread(target=self.run)

    def run(self):
        while True:
            time.sleep(1)
            if self.__alive:
                item = self.queue_.dequeue()
                if item:
                    print("Boarding:", item) # Producer(names)의 queue_의 앞에서부터 Boarding
            else:
                break
        
        print("Consumer is dying.")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()


if __name__ == "__main__":
    
    customers = []
    with open("customer.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            customer = line.split()
            customers.append(customer)

    # FIFO
    names = []
    for c in customers:
        names.append(c[1])

    producer = Producer(names)

    # Priority 
    # producer = Producer(customers)

    consumer = Consumer()
    
    producer.start()
    consumer.start()
    time.sleep(10)
    producer.finish()
    consumer.finish()

