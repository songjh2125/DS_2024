from minheap import *

class Allocator:
    def __init__(self):
        self.chunk_size = 1024 * 4 * 4
        self.total_arena = 0
        self.allocated = 0
        self.free_heap = MinHeap()
        self.allocation_table = {}  # Key: ID, Value: 메모리 블록의 시작주소와 크기
    
    def print_stats(self):
        
        print(f"Arena: {self.total_arena / (1024 * 1024):.2f} MB")
        print(f"In-use: {self.allocated / (1024 * 1024):.2f} MB")
        print(f"Utilization: {self.allocated / self.total_arena:.2f}")
    
    def malloc(self, id, size):
        # free_list에서 적절한 block 찾기
        if self.free_heap.size() > 0:
            for i in range(self.free_heap.size()-1):
                free_size, start = self.free_heap.A[i]
                if free_size >= size:
                    self.free_heap.pop(i)
                    if free_size > size:
                        self.free_heap.insert((free_size - size, start + size))
                    self.allocation_table[id] = (start, size)
                    self.allocated += size
                    return
        
        
        # If no suitable free space is found, allocate a new chunk
        new_addr = self.total_arena
        self.total_arena += self.chunk_size  # Simulate chunk allocation
        self.allocation_table[id] = (new_addr, size)
        self.allocated += size
        
        if self.chunk_size > size:
            self.free_heap.insert((self.chunk_size - size, new_addr + size))
        
        return new_addr
        
    
    def free(self, id):
        if id in self.allocation_table:
            addr, size = self.allocation_table.pop(id)
            self.allocated -= size
            # Add the block to the free list and merge with adjacent free blocks
            self.free_heap.insert((size, addr))

if __name__ == "__main__":
    allocator = Allocator()
    
    import time
    start = time.perf_counter()
    
    with open ("./input.txt", "r") as file:
        n=0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] == 'f':
                allocator.free(int(req[1]))

            if n%100 == 0:
                print(n, "...")
            
            n+=1
    
    end = time.perf_counter()
    elapsed_time_us = (end - start)
    print(f"Elapsed time: {elapsed_time_us:.5f} ms")
    
    allocator.print_stats()