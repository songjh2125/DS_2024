#include <stdio.h>
#include <stdlib.h>

// 노드를 표현하는 구조체
struct ListNode {
    int item;
    struct ListNode *next;
};

// 원형 연결 리스트를 표현하는 구조체
struct CircularLinkedList {
    struct ListNode *tail;
    int numItems;
};

// 노드를 생성하는 함수
struct ListNode* createNode(int item) {
    struct ListNode *newNode = (struct ListNode*)malloc(sizeof(struct ListNode));
    if (newNode == NULL) {
        printf("Memory allocation failed.\n");
        exit(1);
    }
    newNode->item = item;
    newNode->next = NULL;
    return newNode;
}

// 원형 연결 리스트를 초기화하는 함수
void initCircularLinkedList(struct CircularLinkedList *list) {
    list->tail = NULL;
    list->numItems = 0;
}

// 리스트에 새로운 노드를 삽입하는 함수
void insert(struct CircularLinkedList *list, int index, int newItem) {
    // 삽입할 노드 생성
    struct ListNode *newNode = createNode(newItem);
    
    // 빈 리스트일 경우
    if (list->tail == NULL) {
        newNode->next = newNode; // 자기 자신을 가리킴
        list->tail = newNode;
    } else {
        // 이전 노드 찾기
        struct ListNode *prev = list->tail;
        for (int i = 0; i < index; i++) {
            prev = prev->next;
        }
        // 새로운 노드 삽입
        newNode->next = prev->next;
        prev->next = newNode;
        
        // 리스트의 끝에 삽입한 경우 tail 업데이트
        if (index == list->numItems) {
            list->tail = newNode;
        }
    }
    list->numItems++;
}

// 리스트의 모든 노드를 출력하는 함수
void printList(struct CircularLinkedList *list) {
    if (list->tail == NULL) {
        printf("Empty list.\n");
        return;
    }
    
    struct ListNode *curr = list->tail->next; // 시작 노드
    do {
        printf("%d ", curr->item);
        curr = curr->next;
    } while (curr != list->tail->next); // 마지막 노드까지 반복
    printf("\n");
}

int main() {
    struct CircularLinkedList list;
    initCircularLinkedList(&list);
    
    // 리스트에 노드 삽입
    insert(&list, 0, 5);
    insert(&list, 1, 10);
    insert(&list, 1, 8);
    insert(&list, 3, 15);
    
    // 리스트 출력
    printf("List: ");
    printList(&list);
    
    return 0;
}
