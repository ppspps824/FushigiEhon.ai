import streamlit as st


def settings():
    _, center, _ = st.columns([1, 2, 1])

    with center:
        st.session_state.api_key = st.text_input(
            "OpenAI APIキー",
            type="password",
            help="APIキーを設定するとより性能の高いAIを利用できます。",
        )

        text_models = ["gpt-4-1106-preview", "gpt-3.5"]
        image_models = ["dall-e-3", "dall-e-2"]

        st.session_state.text_model = st.selectbox(
            "テキスト生成モデル", options=text_models, key="text_model_selectbox"
        )
        st.session_state.image_model = st.selectbox(
            "イラスト生成モデル", options=image_models, key="image_model_selectbox"
        )

        st.session_state.disable_audio = st.toggle(
            "音声なし", help="テキストの読み上げなし"
        )

        st.write("問い合わせ先: papasim824@gmail.com")
