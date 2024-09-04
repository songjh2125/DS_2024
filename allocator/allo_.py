import heapq

class Allocator:
    def __init__(self, chunk_size=16384):
        self.chunk_size = chunk_size 
        self.free_space = []  # 자유 공간을 관리하기 위한 힙
        self.allocated = {}  # 할당된 메모리 
        self.total_allocated = 0
        self.total_arena_size = 0
        self.tryn = 0
        self.allo12 = 0
        self.allonew = 0
        self.allo99 = 0
    
    def __percolateDown(self, i:int):
        child = 2 * i + 1  # left child
        right = 2 * i + 2  # right child
        if (child <= len(self.free_space)-1):
            if (right <= len(self.free_space)-1 and self.free_space[child] > self.free_space[right]):
                child = right  # index of larger child
            if self.free_space[i] > self.free_space[child]:
                self.free_space[i], self.free_space[child] = self.free_space[child], self.free_space[i]
                self.__percolateDown(child)  
    
    def malloc(self, id, size):
        self.tryn += 1
        if self.free_space:
            for i in range(len(self.free_space)): # free_space 내려가며 적절한 블록을 찾음
                free_size, start = self.free_space[i]
                if free_size >= size:
                    if i <= len(self.free_space)/2:
                        self.allo12 += 1
                    #if i <= 2*len(self.free_space)/3:
                    #    self.allo23 += 1
                    if len(self.free_space)/2 < i < len(self.free_space):
                        self.allo99 += 1
                    self.free_space.pop(i)
                    a, b = self.free_space.pop()
                    self.free_space.insert(i, (a, b))
                    self.__percolateDown(i)
                    if free_size > size:
                        heapq.heappush(self.free_space, (free_size - size, start + size))
                    self.allocated[id] = (start, size)
                    self.total_allocated += size
                    return
            
        new_start = self.total_arena_size # 적절한 블록을 찾지 못한 경우
        self.total_arena_size += self.chunk_size
        if self.chunk_size > size:
            heapq.heappush(self.free_space, (self.chunk_size - size, new_start + size))
        self.allocated[id] = (new_start, size)
        self.total_allocated += size
    
    def free(self, id):
        if id in self.allocated:
            start, size = self.allocated.pop(id)
            self.total_allocated -= size
            self._add_free_block(start, size)

    def _add_free_block(self, start, size):
        heapq.heappush(self.free_space, (size, start))
    
    def print_stats(self):
        arena_size_mb = self.total_arena_size / (1024 * 1024)
        in_use_mb = self.total_allocated / (1024 * 1024)
        utilization = self.total_allocated / self.total_arena_size if self.total_arena_size > 0 else 0
        print("Arena : %.2f MB" % arena_size_mb)
        print("In-use : %.2f" % in_use_mb)
        print("Utilization : %.2f" % utilization)
        print("1/2 이전 할당 확률", self.allo12/self.tryn)
        #print("2/3 이전 할당 확률", self.allo23/self.tryn)
        print("1/2 이후 할당 확률", self.allo99/self.tryn)

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
    print(f"Elapsed time: {elapsed_time_us:.5f} s")
    
    allocator.print_stats()
