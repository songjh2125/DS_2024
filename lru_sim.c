#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CACHE_SIZE_INCREMENT 100
#define MAX_CACHE_SIZE 1000

typedef struct Node {
    int key;
    struct Node* next;
} Node;

Node* head = NULL;
Node* tail = NULL;

void initialize_cache() {
    head = NULL;
    tail = NULL;
}

Node* find_node(int key) {
    Node* current = head;
    while (current != NULL) {
        if (current->key == key) {
            return current;
        }
        current = current->next;
        if (current == head) {
            break;
        }
    }
    return NULL;
}

void insert_node(int key) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    new_node->key = key;
    if (head == NULL) {
        head = new_node;
        tail = new_node;
        new_node->next = new_node;
    }
    else {
        new_node->next = head;
        tail->next = new_node;
        tail = new_node;
    }
}

void remove_node(Node* node) {
    if (node == head) {
        if (head->next == head) {
            head = NULL;
            tail = NULL;
        }
        else {
            head = head->next;
            tail->next = head;
        }
    }
    else {
        Node* current = head;
        while (current->next != node) {
            current = current->next;
        }
        current->next = node->next;
        if (node == tail) {
            tail = current;
        }
    }
    free(node);
}

void evict_node() {
    Node* evict = tail;
    remove_node(evict);
}

void move_to_front(int key) {
    Node* node = find_node(key);
    if (node != NULL) {
        if (node != head) {
            remove_node(node);
            insert_node(node->key);
        }
    }
}

void simulate_cache(FILE* fp, int cache_size) {
    int cache_hit = 0;
    int total_access = 0;
    int* cache = (int*)malloc(cache_size * sizeof(int));
    memset(cache, -1, cache_size * sizeof(int));

    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        int key = atoi(strtok(line, " "));
        int i;
        int found = 0;
        for (i = 0; i < cache_size; i++) {
            if (cache[i] == key) {
                found = 1;
                cache_hit++;
                break;
            }
        }
        if (!found) {
            for (i = cache_size - 1; i > 0; i--) {
                cache[i] = cache[i - 1];
            }
            cache[0] = key;
        }
        total_access++;
    }

    free(cache);

    printf("cache_slot = %d cache_hit = %d ", cache_size, cache_hit);
    if (total_access != 0) {
        printf("hit ratio = %.5f\n", (float)cache_hit / total_access);
    }
    else {
        printf("No accesses.\n");
    }
}


int main() {
    FILE* fp = fopen("linkbench.trc", "r");
    if (fp == NULL) {
        printf("파일을 열 수 없습니다.\n");
        return 1;
    }

    int cache_size;
    for (cache_size = CACHE_SIZE_INCREMENT; cache_size <= MAX_CACHE_SIZE; cache_size += CACHE_SIZE_INCREMENT) {
        initialize_cache();
        simulate_cache(fp, cache_size);
        rewind(fp);
    }

    fclose(fp);

    return 0;
}
