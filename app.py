import os

import const
import openai
import streamlit as st
from modules.create import create
from modules.play import play
from PIL import Image
from streamlit_card import card
from streamlit_option_menu import option_menu
from streamlit_supabase_auth import login_form, logout_button


def guest_login():
    st.session_state.is_guest = True


def init_state():
    st.session_state.is_login = False
    st.session_state.is_guest = False
    st.session_state.user_id = ""
    st.session_state.email = ""
    st.session_state.disable_audio = False
    st.session_state.session = None

    # create
    st.session_state.tales = {
        "title": "",
        "number_of_pages": 3,
        "characters_per_page": const.CHARACTORS_PER_PAGE,
        "sentence_structure": "バランス",
        "age_group": "1～2歳",
        "character_set": "ひらがなのみ",
        "description": "",
        "theme": "",
        "characters": {
            "lead": {
                "name": "",
                "appearance": "",
            },
            "others": [
                {
                    "name": "",
                    "appearance": "",
                },
            ],
        },
        "content": [],
    }
    st.session_state.images = {"title": "", "content": []}
    st.session_state.audios = []
    st.session_state.not_modify = True

    # ai
    st.session_state.text_model = "gpt-4-1106-preview"
    st.session_state.image_model = "dall-e-3"


def main():
    if "is_login" not in st.session_state:
        init_state()

    st.set_page_config(
        page_title="ふしぎえほん.ai",
        page_icon=Image.open("assets/logo.png"),
        layout="wide",
    )

    st.markdown(
        const.HIDE_ST_STYLE,
        unsafe_allow_html=True,
    )

    os.environ["SUPABASE_KEY"] = st.secrets["SUPABASE_API_KEY"]

    # Welcomページ
    if not st.session_state.is_login:
        title_image_cols = st.columns([1, 8])
        with title_image_cols[0]:
            st.image("assets/header.png")
        ## About
        st.image("assets/title_back.png")
        title_cols = st.columns([3, 1])
        with title_cols[0]:
            card_cols = st.columns(2)

            with card_cols[0]:
                card(
                    title="簡単かつ柔軟",
                    text=[
                        "タイトルを入力するだけで",
                        "物語・イラスト・音声すべてをAIが生成します。",
                    ],
                    styles=const.TITLE_BOX_STYLE,
                    key="card1-1",
                )
                card(
                    title="オリジナリティ",
                    text=[
                        "手持ちの写真やイラストをアップロードすることもでき",
                        "AIによって画像をグレードアップすることもできます。",
                    ],
                    styles=const.TITLE_BOX_STYLE,
                    key="card1-2",
                )
            with card_cols[1]:
                card(
                    title="いつでもどこでも",
                    text=[
                        "作成した絵本はクラウド上に保存でき",
                        "動画やPDFでダウンロードすることもできます。",
                    ],
                    styles=const.TITLE_BOX_STYLE,
                    key="card2-1",
                )
                card(
                    title="すべてが無料",
                    text=[
                        "すべての機能は無料で利用できます。",
                        "クレジットを使い切ったら追加できます。",
                    ],
                    styles=const.TITLE_BOX_STYLE,
                    key="card2-2",
                )
            title_inner_cols = st.columns(2)
            with title_inner_cols[0]:
                st.video("assets/title_movie1.mp4")
            with title_inner_cols[1]:
                st.video("assets/title_movie2.mp4")

        ## Login
        with title_cols[1]:
            with st.container(border=True):
                st.session_state.session = login_form(
                    url=st.secrets["SUPABASE_URL"],
                    providers=["google"],
                )
                st.button("Free Trial", on_click=guest_login)

        if all([not st.session_state.session, not st.session_state.is_guest]):
            return

        st.experimental_set_query_params(page=["success"])
        st.session_state.is_login = True
        st.rerun()

    # ログイン後画面
    if st.session_state.is_guest:
        st.session_state.user_id = "guest"
        st.session_state.email = "Free Trial"
    else:
        st.session_state.user_id = st.session_state.session["user"]["id"]
        st.session_state.email = st.session_state.session["user"]["email"]

    openai.api_key = st.secrets["OPEN_AI_KEY"]

    header_cols = st.columns([1, 3, 1])
    header_cols[0].image("assets/header.png")
    header_cols[2].caption(f"logged in {st.session_state.email}")
    with st.sidebar:
        selected = option_menu(
            None,
            ["よむ", "つくる", "ログアウト"],
            icons=["bi-play-btn", "bi-brush", "bi-door-open"],
            menu_icon=None,
            default_index=0,
            orientation="vartical",
            styles={
                "container": {
                    "margin": "0px !important",
                    "background-color": "#fafafa",
                },
                "icon": {"color": "fafafa", "font-size": "25px"},
                "nav-link": {
                    "font-size": "20px",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "004a55"},
            },
        )
    if selected == "つくる":
        create()
    elif selected == "よむ":
        play()
    elif selected == "ログアウト":
        logout_button()
        init_state()
        st.rerun()


if __name__ == "__main__":
    main()
