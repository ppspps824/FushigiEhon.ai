import streamlit as st


def about():
    with st.expander("えほんをつくる"):
        st.write("えほんをつくる")
    with st.expander("えほんをよむ"):
        st.write("えほんをつくる")
    with st.expander("APIキーの取得方法"):
        st.write("OpenAIのサイトで取得")
