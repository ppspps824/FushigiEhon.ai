import streamlit as st


def about():
    with st.container(border=True):
        st.write("**ふしぎえほん.aiとは**")
        [st.write("") for _ in range(10)]

    col1, col2, col3 = st.columns(3)
    with col1.container(border=True):
        st.write("**えほんをつくる**")
        [st.write("") for _ in range(15)]
    with col2.container(border=True):
        st.write("**えほんをみる**")
        [st.write("") for _ in range(15)]
    with col3.container(border=True):
        st.write("**せってい**")
        [st.write("") for _ in range(15)]
