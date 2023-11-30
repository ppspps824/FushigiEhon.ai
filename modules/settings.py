import streamlit as st


def settings():
    _, center, _ = st.columns([1, 2, 1])

    with center:
        st.session_state.api_key = st.text_input(
            "OpenAI APIキー",
            type="password",
            help="APIキーを設定するとより性能の高いAIを利用できます。",
        )
        st.session_state.disable_audio = st.toggle(
            "音声なし", help="テキストの読み上げなし"
        )

        st.write("問い合わせ先: papasim824@gmail.com")
