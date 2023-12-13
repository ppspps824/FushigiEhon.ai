import streamlit as st


def settings():
    left, center, right = st.columns(3)

    with left:
        left_container = st.container(border=True)
        with left_container:
            st.write("えほんをよむの設定")
            st.session_state.disable_audio = st.toggle(
                "音声なし", help="テキストの読み上げなし"
            )
            [st.write("") for _ in range(17)]

    with right:
        right_container = st.container(border=True)
        with right_container:
            st.write("その他")
            st.write("問い合わせ: papasim824@gmail.com")
            [st.write("") for _ in range(17)]
