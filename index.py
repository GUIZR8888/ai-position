import st
import streamlit as st

st.title("AI大模型网站")

col,col1 = st.columns(2)
with col:
    st.image("https://aigc-files.bigmodel.cn/api/cogview/20241029224551cb89a9b41407416a_0.png")
    flag = st.button("撇砍",use_container_width=True)
    if flag:
        st.switch_page("pages/textToPeople.py")

with col1:
    st.image("https://aigc-files.bigmodel.cn/api/cogview/20241029224551cb89a9b41407416a_0.png")
    flag1 = st.button("个划个划",use_container_width=True)
    if flag1:
        st.switch_page("pages/textToPicture.py")