import const
import openai
import streamlit as st
from modules.create import create
from modules.play import play
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_supabase_auth import login_form


def guest_login():
    st.session_state.is_guest = True


def main():
    if "is_login" not in st.session_state:
        st.session_state.is_login = False
        st.session_state.is_guest = False
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

    layout = (
        "wide"
        if any([st.session_state.is_login, st.session_state.is_guest])
        else "centered"
    )

    st.set_page_config(
        page_title="ふしぎえほん.ai",
        page_icon=Image.open("assets/logo.png"),
        layout=layout,
    )

    st.markdown(
        const.HIDE_ST_STYLE,
        unsafe_allow_html=True,
    )

    title_place = st.empty()
    with title_place:
        title_cols = st.columns([1, 3, 1])
        with title_cols[1]:
            st.image("assets/title.png")

    session = ""
    if not st.session_state.is_guest:
        session = login_form(
            url=st.secrets["SUPABASE_URL"],
            apiKey=st.secrets["SUPABASE_API_KEY"],
            providers=["google", "twitter"],
        )

    guest_place = st.empty()
    guest_place.button("ゲストログイン", on_click=guest_login, type="primary")

    if all([not session, not st.session_state.is_guest]):
        return

    st.experimental_set_query_params(page=["success"])
    title_place.empty()
    guest_place.empty()

    st.session_state.is_login = True

    if st.session_state.is_guest:
        st.session_state.user_id = "guest"
        st.session_state.email = "ゲスト"
    else:
        st.session_state.user_id = session["user"]["id"]
        st.session_state.email = session["user"]["email"]

    openai.api_key = st.secrets["OPEN_AI_KEY"]

    header_cols = st.columns([1, 3, 1])
    header_cols[0].image("assets/header.png")
    header_cols[2].caption(f"logged in {st.session_state.email}")

    selected = option_menu(
        None,
        ["よむ", "つくる"],
        icons=["bi-play-btn", "bi-brush"],
        menu_icon=None,
        default_index=0,
        orientation="horizontal",
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


if __name__ == "__main__":
    main()
