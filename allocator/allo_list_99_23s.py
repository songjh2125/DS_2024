# Best Fit
# free_list를 free size가 작은 순서로 정렬 후 앞에서부터 탐색 (약 70s, 162.19/167.37(0.97))

class Allocator:
    def __init__(self):
        self.chunk_size = 1024 * 4
        self.arena = []
        self.free_list = [] # free space를 관리하는 리스트
        self.allocation_map = {}  # Key: 메모리 블록 시작주소, Value: 메모리 블록의 크기와 상태
        self.allocation_table = {}  # Key: ID, Value: 메모리 블록의 시작주소와 크기
    
    def print_stats(self):
        total_allocated = sum(size for _, (size, status) in self.allocation_map.items() if status == 'allocated')
        total_arena = len(self.arena) * self.chunk_size
        
        print(f"Arena: {total_arena / (1024 * 1024):.2f} MB")
        print(f"In-use: {total_allocated / (1024 * 1024):.2f} MB")
        print(f"Utilization: {total_allocated / total_arena:.2f}")


    def malloc(self, id, size):
        # free_list에서 적절한 block 찾기
        for i, (addr, free_size) in enumerate(self.free_list):
            if free_size >= size:
                # 메모리 할당
                self.allocation_map[addr] = (size, 'allocated')
                self.allocation_table[id] = (addr, size)
                
                # free_list 업데이트
                if free_size > size:
                    self.free_list[i] = (addr + size, free_size - size)
                else:
                    self.free_list.pop(i)
                return addr
        
        # 적절한 free space가 없으면 새로운 chunk 할당
        new_addr = len(self.arena) * self.chunk_size
        self.arena.append([False] * self.chunk_size)  # arena에 청크 추가
        self.allocation_map[new_addr] = (size, 'allocated')
        self.allocation_table[id] = (new_addr, size)
        
        # 남은 공간을 free space에 추가
        if self.chunk_size > size:
            self.free_list.append((new_addr + size, self.chunk_size - size))
        
        return new_addr
    
    def free(self, id):
        if id in self.allocation_table:
            addr, size = self.allocation_table.pop(id)
            self.allocation_map.pop(addr)
            
            # 해제된 공간을 free_list에 추가
            self.free_list.append((addr, size))
            self.free_list.sort(key= lambda x:x[1]) # 크기순 정렬

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