import heapq

class Allocator:
    def __init__(self, chunk_size=16384):
        self.chunk_size = chunk_size 
        self.free_space = []  # 자유 공간을 관리하기 위한 힙
        self.allocated = {}  # 할당된 메모리 
        self.total_allocated = 0
        self.total_arena_size = 0
    
    def malloc(self, id, size):
        tp = []
        while self.free_space: # 적절한 자유 블록을 찾음
            free_size, start = heapq.heappop(self.free_space)
            if free_size >= size:
                for i in range(len(tp)):
                    st, siz = tp[i]
                    heapq.heappush(self.free_space, (st, siz))
                if free_size > size:
                    heapq.heappush(self.free_space, (free_size - size, start + size))
                self.allocated[id] = (start, size)
                self.total_allocated += size
                return
            tp.append((free_size, start))
        
        
        for i in range(len(tp)):
            st, siz = tp[i]
            heapq.heappush(self.free_space, (st, siz))
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

