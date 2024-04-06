from queue_.listQueue import ListQueue
import threading
import time

class Producer:
    def __init__(self, items):
        self.__alive = True
        self.items = items
        self.pos = 0
        self.queue_1 = ListQueue() # 일반
        self.queue_2 = ListQueue() # 골드
        self.queue_3 = ListQueue() # 플래티넘
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
                if item:  # Producer의 3개의 queue 중 등급에 맞는 queue에 도착한 순서대로 enqueue 
                    if int(item[0]) == 1:
                        self.queue_1.enqueue(item)
                        print("Arrived:", item[0], item[1])
                    if int(item[0]) == 2:
                        self.queue_2.enqueue(item)
                        print("Arrived:", item[0], item[1])
                    if int(item[0]) == 3:
                        self.queue_3.enqueue(item)
                        print("Arrived:", item[0], item[1])
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
        self.queue_1 = producer.queue_1 # Producer(costomers)의 queue들을 이용
        self.queue_2 = producer.queue_2
        self.queue_3 = producer.queue_3
        self.worker = threading.Thread(target=self.run)

    def run(self):
        while True:
            time.sleep(1)
            if self.__alive:  # Producer(costomers)의 queue들에서 도착순, 등급순으로 Boarding
                if not self.queue_3.isEmpty():
                    item = self.queue_3.dequeue()
                    print("Boarding:", item[0], item[1])
                elif not self.queue_2.isEmpty():
                    item = self.queue_2.dequeue()
                    print("Boarding:", item[0], item[1])
                elif not self.queue_1.isEmpty():
                    item = self.queue_1.dequeue()
                    print("Boarding:", item[0], item[1])                
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

    # producer = Producer(names)
    
    # Priority 
    producer = Producer(customers)

    consumer = Consumer()
    
    producer.start()
    consumer.start()
    time.sleep(10)
    producer.finish()
    consumer.finish()

