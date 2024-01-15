import os

import streamlit as st
import streamlit_antd_components as sac
from PIL import Image
from streamlit_card import card
from streamlit_option_menu import option_menu
from streamlit_supabase_auth import login_form, logout_button

import const
import modules.database as db
from modules.create import create
from modules.database import *
from modules.play import play
from modules.setting import setting


def init_state():
    st.session_state.user_id = ""
    st.session_state.email = ""
    st.session_state.disable_audio = False

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
    if "user_id" not in st.session_state:
        init_state()

    st.set_page_config(
        page_title="ふしぎえほん.ai",
        page_icon=Image.open("assets/logo.webp"),
        layout="wide",
    )

    st.markdown(
        const.HIDE_ST_STYLE,
        unsafe_allow_html=True,
    )

    os.environ["SUPABASE_KEY"] = st.secrets["SUPABASE_API_KEY"]

    title_logo_cols = st.columns([1, 8])
    title_image_place = st.empty()

    title_cols = st.columns([3, 1])
    with title_cols[1]:
        session = login_form(
            url=st.secrets["SUPABASE_URL"],
            providers=["google"],
        )

    ## Login
    if not session:
        # Welcomページ
        with title_logo_cols[0]:
            st.image("assets/header.webp")
        ## About
        with title_image_place:
            st.image("assets/title_back.webp")

        with title_cols[0]:
            card_cols = st.columns(2)

            with card_cols[0]:
                card(
                    title="かんたん",
                    text=[
                        "タイトルを入力するだけですべてをAIが生成します。",
                        "何度でも自由に編集ができます。",
                    ],
                    styles=const.TITLE_BOX_STYLE,
                    key="card1-1",
                )
                card(
                    title="じぶんだけの",
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
                    title="さいしょからぜんぶ",
                    text=[
                        "初回ログイン時に100クレジットが付与されるので、すぐにすべての機能を利用できます。",
                        "※クレジットはイラスト生成でのみ消費します。",
                    ],
                    styles=const.TITLE_BOX_STYLE,
                    key="card2-2",
                )
            step_num = sac.steps(
                items=[
                    sac.StepsItem(
                        title="どきどき。きょうのおはなし",
                        subtitle="タイトルだけで絵本を作ろう",
                    ),
                    sac.StepsItem(
                        title="きらきら！そうぞうがあふれだす",
                        subtitle="あなたのアイディアが、ページごとに生き生きとしたイラストになります。",
                    ),
                    sac.StepsItem(
                        title="にこにこ。おもいでえほん",
                        subtitle="楽しかった一日を、写真と一緒に絵本にしよう。",
                    ),
                    sac.StepsItem(
                        title="わくわく！みんなとだいぼうけん。",
                        subtitle="家族、お友達、私！みんなで大冒険するお話を作ろう。",
                    ),
                ],
                format_func="title",
                placement="vertical",
                return_index=True,
                dot=True,
            )
            # card(
            #     title="すぐに始める",
            #     text="",
            #     styles=const.TITLE_LINK_BOX_STYLE,
            #     key="card",
            #     on_click=guest_login
            # )

            if step_num == 0:
                st.video("https://youtu.be/1TiL2p5WSeQ?feature=shared")
            elif step_num == 1:
                st.video("https://youtu.be/qSV2wck61nc?feature=shared")
            elif step_num == 2:
                st.video("https://youtu.be/tNwTA9wSVkM?feature=shared")
            elif step_num == 3:
                st.video("https://youtu.be/ZZDwx4V__0I?feature=shared")

        ## ライセンス表記
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("---")
        st.caption("© 2023- ふしぎえほん.ai All Rights Reserved.")
        st.link_button("特定商取引法に基づく表記", url=const.LEGAL)

        return

    st.experimental_set_query_params(page=["success"])

    # ログイン後画面
    st.session_state.user_id = session["user"]["id"]
    st.session_state.email = session["user"]["email"]
    user_info = db.read_user(st.session_state.user_id)
    if not user_info.data:
        db.create_user(user_id=st.session_state.user_id, email=st.session_state.email)
        db.adding_credits(user_id=st.session_state.user_id, event="新規登録", value=-50)

    header_cols = st.columns([1, 3, 1])
    header_cols[0].image("assets/header.webp")
    header_cols[2].caption(f"logged in {st.session_state.email}")

    menu_options = ["よむ", "つくる", "設定"]
    menu_icons = ["bi-play-btn", "bi-brush", "bi-gear"]

    with st.sidebar:
        selected = option_menu(
            None,
            menu_options,
            icons=menu_icons,
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
        logout_button()
        with st.container(border=True):
            credits_info = db.read_credits(st.session_state.user_id)
            credits = abs(sum([info["value"] for info in credits_info.data]))
            st.caption(f"クレジット残量：{credits}")
            st.link_button(
                "クレジット購入",
                url=st.secrets["stripe_link"]
                + "?prefilled_email="
                + st.session_state.email,
            )
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        ## ライセンス表記
        st.caption("© 2023- ふしぎえほん.ai All Rights Reserved.")
        st.caption("Contact fushigiehon@gmail.com")
        st.link_button("特定商取引法に基づく表記", url=const.LEGAL)
    if selected == "つくる":
        create()
    elif selected == "よむ":
        play()
    elif selected == "戻る":
        logout_button()
        init_state()
        st.rerun()

    elif selected == "設定":
        setting()


if __name__ == "__main__":
    main()
