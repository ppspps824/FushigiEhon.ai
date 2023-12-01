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

    with center:
        center_container = st.container(border=True)
        with center_container:
            st.write("AI機能の設定")
            st.session_state.api_key = st.text_input(
                "OpenAI APIキー",
                type="password",
                help="APIキーを設定するとより性能の高いAIを利用できます。",
            )
            with st.expander("APIキーの取得方法"):
                st.write("")

            text_models = ["gpt-4-1106-preview", "gpt-3.5"]
            image_models = ["dall-e-3", "dall-e-2"]

            st.session_state.text_model = st.selectbox(
                "テキスト生成モデル", options=text_models, key="text_model_selectbox"
            )
            st.session_state.image_model = st.selectbox(
                "イラスト生成モデル", options=image_models, key="image_model_selectbox"
            )

    with right:
        right_container = st.container(border=True)
        with right_container:
            st.write("その他")
            st.write("問い合わせ: papasim824@gmail.com")
            [st.write("") for _ in range(17)]
