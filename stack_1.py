from stack.listStack import *

def reverse(str):
    st = ListStack()
    for i in range(str):
        st.push(str[i])
    out = ""
    while not st.isEmpty():
        out += st.pop()
    return out
