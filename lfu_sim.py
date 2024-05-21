class LPNFrequency:
    def __init__(self):
        self.__frequency = {}  # LPN과 그 frequency를 저장하는 딕셔너리
    
    # frequency 딕셔너리의 빈도수를 업데이트 하는 메서드
    def update(self, lpn):
        if lpn in self.__frequency:
            self.__frequency[lpn] += 1  # LPN이 이미 존재할 경우 빈도수 1 증가
        else:
            self.__frequency[lpn] = 1  # LPN이 존재하지 않을 경우 그 LPN의 빈도수 1로 설정
    
    # LPN의 빈도수를 반환하는 메서드
    def get_frequency(self, lpn):
        return self.__frequency.get(lpn, 0)
    
    
class MinHeap:
    def __init__(self, *args):
        if len(args) != 0:
            self.__A = args[0]  # 파라미터로 온 리스트
        else:
            self.__A = []
        self.__frequency = LPNFrequency()  # MinHeap 에서 사용할 딕셔너리
    
    # MinHeap의 LPN 빈도수를 업데이트 하는 메서드
    def update_frequency(self, lpn):
        self.__frequency.update(lpn)
    
    # MinHeap의 LPN의 빈도수를 반환하는 메서드
    def get_frequency(self, lpn):
        return self.__frequency.get_frequency(lpn)
    
    # 힙에 원소 삽입하기 (재귀 알고리즘 버전)
    def insert(self, x):
        self.__A.append(x)
        self.update_frequency(x) # 원소 삽입후 frequency 딕셔너리 업데이트
        self.__percolateUp(len(self.__A)-1)
    
    # 스며오르기
    def __percolateUp(self, i:int):
        parent = (i - 1) // 2
        if i > 0 and self.get_frequency(self.__A[i]) < self.get_frequency(self.__A[parent]):
            self.__A[i], self.__A[parent] = self.__A[parent], self.__A[i]
            self.__percolateUp(parent)
    
    # 힙에서 원소 삭제하기
    def deleteMin(self):
        if (not self.isEmpty()):
            min = self.__A[0]
            self.__A[0] = self.__A.pop()  # *.pop(): 리스트의 끝원소 삭제 후 원소 리턴
            self.percolateDown(0)
            return min
        else:
            return None
    
    # 스며내리기
    def percolateDown(self, i:int):
        child = 2 * i + 1  # left child
        right = 2 * i + 2  # right child
        if (child <= len(self.__A)-1):
            if (right <= len(self.__A)-1 and self.get_frequency(self.__A[child]) > self.get_frequency(self.__A[right])):
                child = right  # index of larger child
            if self.get_frequency(self.__A[i]) > self.get_frequency(self.__A[child]):
                self.__A[i], self.__A[child] = self.__A[child], self.__A[i]
                self.percolateDown(child)
    
    def min(self):
        return self.__A[0]
    
    # 힙 만들기
    def buildHeap(self):
        for i in range((len(self.__A) - 2) // 2, -1, -1):
            self.percolateDown(i)
    
    def isEmpty(self) -> bool:
        return len(self.__A) == 0
    
    def clear(self):
        self.__A = []
    
    def size(self) -> int:
        return len(self.__A)
    
    # x값의 인덱스를 반환하는 메서드
    def index(self, x):
        return self.__A.index(x)
    
    def __iter__(self):
        return iter(self.__A)
    
    def heapPrint(self):
        pass
    

def lfu_sim(cache_slots):
    cache_hit = 0
    tot_cnt = 0
    cache = MinHeap()
    
    data_file = open("linkbench.trc")
    
    for line in data_file.readlines():
        lpn = line.split()[0]
        
        tot_cnt += 1
        
        if lpn in cache:  # hit
            cache.update_frequency(lpn)
            cache.percolateDown(cache.index(lpn))
            cache_hit += 1
        else:  # miss
            if cache.size() >= cache_slots:
                cache.deleteMin()
            cache.insert(lpn)
    
    print("cache_slot = ", cache_slots, "cache_hit = ", cache_hit, "hit_ratio = ", cache_hit/ tot_cnt)


if __name__ == "__main__":
    for cache_slots in range(100, 1000, 100):
        lfu_sim(cache_slots)