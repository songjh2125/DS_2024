from queue_.listQueue import *

class ListStack:
    def __init__(self):
        self.__stack = ListQueue()
    
    def push(self, x):
        self.__stack.enqueue(x)
    
    def pop(self):
        
        return self.__stack.dequeue()