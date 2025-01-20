data_list = list(map(int, input("10개의 숫자를 입력하시오.").split()))


# 재귀 버전
def find_max_recursive(list):
    if len(list) > 1:
        mid = len(list) // 2
        L = list[:mid]
        R = list[mid:]

        find_max_recursive(L)  # partion된 L을 sort
        find_max_recursive(R)  # partion된 R을 sort

    # sorting 된 L과 R을 통합

        list.clear()  # list 내용 비우기
        while len(L) > 0 and len(R) > 0:
            if L[0] >= R[0]:
                list.append(L[0])
                L.pop(0)
            else:
                list.append(R[0])
                R.pop(0)

        for i in L:
            list.append(i)
        for i in R:
            list.append(i)
    
    return list



# 반복 버전
def find_max_iterative(list):

    for i in range(len(list)):
        # Find the maximum element in remaining unsorted array
        max_idx = i
        for j in range(i + 1, len(list)):
            if list[max_idx] < list[j]:
                max_idx = j
        # Swap the found maximum element with the first element
        list[i], list[max_idx] = list[max_idx], list[i]
    
    return list

print(find_max_iterative(data_list.copy()))
print(find_max_recursive(data_list.copy()))