from math import log2

class Heap:
	def __init__(self, *args):
		if len(args) != 0:
			self.__A = args[0] # 파라미터로 온 리스트
		else:
			self.__A = []
 
	# [알고리즘 8-2] 구현: 힙에 원소 삽입하기(재귀 알고리즘 버전)
	def insert(self, x):
		self.__A.append(x)
		self.__percolateUp(len(self.__A)-1)

	# 스며오르기
	def __percolateUp(self, i:int):
		parent = (i - 1) // 2
		if i > 0 and self.__A[i] > self.__A[parent]:
			self.__A[i], self.__A[parent] = self.__A[parent], self.__A[i]
			self.__percolateUp(parent)

	# [알고리즘 8-2] 구현: 힙에서 원소 삭제하기
	def deleteMax(self):
		# heap is in self.__A[0...len(self.__A)-1]
		if (not self.isEmpty()):
			max = self.__A[0]
			self.__A[0] = self.__A.pop() # *.pop(): 리스트의 끝원소 삭제 후 원소 리턴
			self.__percolateDown(0)
			return max
		else:
			return None

	# 스며내리기
	def __percolateDown(self, i:int):
		# Percolate down w/ self.__A[i] as the root
		child = 2 * i + 1  # left child
		right = 2 * i + 2  # right child
		if (child <= len(self.__A)-1):
			if (right <= len(self.__A)-1 and self.__A[child] < self.__A[right]):
				child = right  # index of larger child
			if self.__A[i] < self.__A[child]:
				self.__A[i], self.__A[child] = self.__A[child], self.__A[i]
				self.__percolateDown(child)

	def max(self):
		return self.__A[0]

	# 힙 만들기
	def buildHeap(self):
		for i in range((len(self.__A) - 2) // 2, -1, -1):
			self.__percolateDown(i)

	# 힙이 비었는지 확인하기
	def isEmpty(self) -> bool:
		return len(self.__A) == 0

	def clear(self):
		self.__A = []

	def size(self) -> int:
		return len(self.__A)

	def heapPrint(self):
		if len(self.__A) == 0:
			return
		h = int(log2(len(self.__A)) + 1)
		max_width = 2 ** h - 1  # 각 레벨의 최대 너비
		max_digits = len(str(max(self.__A)))  # 리스트 내 최대 숫자의 자릿수
		for i in range(h):
			start = 2 ** i - 1  # 각 레벨의 시작 인덱스
			end = min(start * 2 + 1, len(self.__A))  # 각 레벨의 끝 인덱스
			spacing = max_width // (2 ** i)  # 간격 계산
			line = ''
			for j in range(start, end):
				num_str = str(self.__A[j]).center(max_digits, ' ')
				line += num_str
				if j != end - 1:  # 마지막 노드가 아니면 간격을 추가합니다.
					line += ' ' * ((spacing - max_digits) // 2) + ' ' * ((spacing - max_digits) % 2)  # 간격을 채워넣습니다.
			
			print(line.center(max_width * (max_digits + 1) + max_digits))

# 코드 8-8