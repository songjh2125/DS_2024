from stack.listStack import *

def checkReverse(str):
    st = ListStack()
    for i in range(len(str)//2):
        st.push(str[i])
    for i in range(len(str)):
        if st[i] == st.top():
            st.pop()
        else:
            return False
    return True

checkReverse("abc$cba")