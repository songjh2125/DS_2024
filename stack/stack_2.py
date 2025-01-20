from listStack import *

def checkReverse(str):
    st = ListStack()
    for i in range(len(str)//2):
        st.push(str[i])
    
    if len(str) % 2 != 0:
        start = len(str) // 2 + 1
    else:
        start = len(str) // 2


    for i in range(start, len(str)):
        if str[i] == st.top():
            st.pop()
            i += 1
        else:
            return False
    return True



print(checkReverse("abc$cba"))