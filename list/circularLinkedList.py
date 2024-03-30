from list.listNode import ListNode

class CircularLinkedList:
    def __init__(self):
        self.__tail = ListNode("dummy", None)
        self.__tail.next = self.__tail
        self.__numItems = 0
 
    def insert(self, i:int, newItem) -> None:
        if i >= 0 and i <= self.__numItems:
            prev = self.getNode(i - 1)
            newNode = ListNode(newItem, prev.next)
            prev.next = newNode
            if i == self.__numItems:
                self.__tail = newNode
            self.__numItems += 1
        else:
            print("index", i, ": out of bound in insert()") # 필요 시 에러 처리
        
    def append(self, newItem) -> None:
        newNode = ListNode(newItem, self.__tail.next)
        self.__tail.next = newNode
        self.__tail = newNode
        self.__numItems += 1
    
    # [알고리즘 5-3] 구현 : 연결 리스트의 원소 삭제하기
    def pop(self, *args):
        if self.isEmpty():
            return None
        if len(args) != 0:
            i = args[0]
        if len(args) == 0 or i == -1:
            i = self.__numItems - 1
        if (i >= 0 and i <= self.__numItems-1): # i번 노드 삭제. 고정 파라미터
            prev = self.getNode(i - 1)
            retItem = prev.next.item
            prev.next = prev.next.next
            if i == self.__numItems - 1:
                self.__tail = prev
            self.__numItems -= 1
            return retItem
        else:
            return None

    # [알고리즘 5-4] 구현 : 연결 리스트의 원소 x 삭제하기 (더미 헤드를 두는 대표 버전)
    def remove(self, x):
        (prev, curr) = self.__findNode(x)
        if curr != None:
            prev.next = curr.next
            if curr == self.__tail:
                self.__tail = prev
            self.__numItems -= 1
            return x
        else:
            return None
    
    # [알고리즘 5-5] 구현 : 연결 리스트의 고번 원소 알려주기
    def get(self, *args):
        if self.isEmpty():
            return None
        if len(args) != 0:
            i = args[0]
        if len(args) == 0 or i == -1:
            i = self.__numItems - 1
        if (i >= 0 and i <= self .__numItems - 1):
            return self.getNode(i).item
        else:
            return None
    
    # [알고리즘 5-7] 구현 : x가 연결 리스트의 몇 번 원소인지 알려주기
    def index(self, x) -> int:
        cnt = 0
        for element in self:
            if element == x:
                return cnt
            cnt += 1
        return -12345
    
    # [알고리즘 5-8] 구현 : 기타 작업들
    def isEmpty(self) -> bool:
        return self.__numItems == 0
    
    def size(self) -> int:
        return self.__numItems
    
    def clear(self):
        self.__tail = ListNode("dummy", None)
        self.__tail.next = self.__tail
        self.__numItems = 0
    
    def count(self, x) -> int:
        cnt = 0
        for element in self:
            if element == x:
                cnt += 1
        return cnt
        
    def extend(self, a): # a는 순회 가능한 모든 객체
        for x in a:
            self.append(x)
            
    def copy(self) -> 'CircularLinkedList':
        a = CircularLinkedList()
        for element in self:
            a.append(element)
        return a
    
    def reverse(self) -> None:
        __head = self.__tail.next # 더미 헤드
        prev = __head; curr = prev.next; next = curr.next
        curr.next = __head; __head.next = self.__tail; self.__tail = curr
        for i in range(self.__numItems - 1):
            prev = curr; curr = next; next = next.next
            curr.next = prev
            
    def sort(self) -> None:
        a = []
        for element in self:
            a.append(element)
        a.sort()
        self.clear()
        for element in a:
            self.append(element)
            
    def __findNode(self, x) -> (ListNode, ListNode):
        __head = prev = self.__tail.next # 더미 헤드
        curr = prev.next # 0번 노드
        while curr != None:
            if curr.item == x:
                return (prev, curr)
            else:
                prev = curr; curr = curr.next
        return (None, None)

    # [알고리즘 5-6] 구현 : 연결 리스트의 고번 노드 알려주기
    def getNode(self, i:int) -> ListNode:
        curr = self.__tail.next # 더미 헤드, index : -1
        for index in range(i+1):
            curr = curr.next
        return curr
    
    def printList(self):
        for element in self:
            print(element, end = ' ')
        print()
    
    def __iter__(self):    # generating iterator and return
        return CircularLinkedListIterator(self)


class CircularLinkedListIterator:
    def __init__(self, alist):
        self.__head = alist.getNode(-1) # 더미 헤드
        self.iterPosition = self.__head.next # 0번 노드
    def __next__(self):
        if self.iterPosition == self.__head: # 순환 끝
            raise StopIteration
        else: # 현재 원소를 리턴하면서 다음 원소로 이동
            item = self.iterPosition.item
            self.iterPosition = self.iterPosition.next
            return item