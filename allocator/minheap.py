class MinHeap:
    def __init__(self, *args):
        if len(args) != 0:
            self.A = args[0]  # 파라미터로 온 리스트
        else:
            self.A = []
     
    # 힙에 원소 삽입하기 (재귀 알고리즘 버전)
    def insert(self, x):
        self.A.append(x)
        self.__percolateUp(len(self.A)-1)
    
    # 스며오르기
    def __percolateUp(self, i:int):
        parent = (i - 1) // 2
        if i > 0 and self.A[i] < self.A[parent]:
            self.A[i], self.A[parent] = self.A[parent], self.A[i]
            self.__percolateUp(parent)
    
    # 힙에서 원소 삭제하기
    def deleteMin(self):
        if (not self.isEmpty()):
            min = self.A[0]
            self.A[0] = self.A.pop()  # *.pop(): 리스트의 끝원소 삭제 후 원소 리턴
            self.__percolateDown(0)
            return min
        else:
            return None
    
    def pop(self, i):
        if (len(self.A) > 2):
            temp = self.A[i]
            self.A[i] = self.A.pop()  # *.pop(): 리스트의 끝원소 삭제 후 원소 리턴
            self.__percolateDown(i)
            return temp
        else:
            return None
    
    # 스며내리기
    def __percolateDown(self, i:int):
        child = 2 * i + 1  # left child
        right = 2 * i + 2  # right child
        if (child <= len(self.A)-1):
            if (right <= len(self.A)-1 and self.A[child] > self.A[right]):
                child = right  # index of larger child
            if self.A[i] > self.A[child]:
                self.A[i], self.A[child] = self.A[child], self.A[i]
                self.__percolateDown(child)
    
    def min(self):
        return self.A[0]
    
    # 힙 만들기
    def buildHeap(self):
        for i in range((len(self.A) - 2) // 2, -1, -1):
            self.__percolateDown(i)
    
    def isEmpty(self) -> bool:
        return len(self.A) == 0
    
    def clear(self):
        self.A = []
    
    def size(self) -> int:
        return len(self.A)
    
    # x값의 인덱스를 반환하는 메서드
    def index(self, x):
        return self.A.index(x)
    
    def __iter__(self):
        return iter(self.A)
    
    def heapPrint(self):
        pass